import secrets

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session

from app.core.config import settings
from app.core.security import ALGORITHM
from app.database.db import engine
from app.enums.role_enum import UserRole
from app.repositories.user import get_user_by_email
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if not isinstance(email, str):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with Session(engine) as session:
        user = get_user_by_email(session, email)
    if user is None:
        raise credentials_exception
    return user


def require_roles(*allowed_roles: UserRole):
    def role_guard(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return current_user

    return role_guard


def is_bot_request(x_bot_key: str | None) -> bool:
    """True when the request carries the shared bot key. With no key
    configured, only local development trusts the bot."""
    if not settings.BOT_API_KEY:
        return settings.ENVIRONMENT == "local"
    return bool(x_bot_key) and secrets.compare_digest(x_bot_key, settings.BOT_API_KEY)


def require_bot(x_bot_key: str | None = Header(default=None)) -> None:
    if not is_bot_request(x_bot_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing bot key",
        )


def require_roles_or_bot(*allowed_roles: UserRole):
    """Allow either the WhatsApp bot (X-Bot-Key header) or a logged-in user
    with one of the given roles. Returns the user, or None for the bot."""

    def guard(
        x_bot_key: str | None = Header(default=None),
        token: str | None = Depends(optional_oauth2_scheme),
    ) -> User | None:
        if x_bot_key is not None and is_bot_request(x_bot_key):
            return None
        user = get_current_user(token)
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return user

    return guard

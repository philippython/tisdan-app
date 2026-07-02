from datetime import datetime, timedelta
from typing import Any
import hashlib
import bcrypt
from jose import jwt

from app.core.config import settings

ALGORITHM = "HS256"


def _bcrypt_sha256_password(password: str) -> bytes:
    raw_bytes = password.encode("utf-8")
    return hashlib.sha256(raw_bytes).digest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = _bcrypt_sha256_password(plain_password)
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    password_bytes = _bcrypt_sha256_password(password)
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

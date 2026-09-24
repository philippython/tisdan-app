from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles, require_roles_or_bot
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.referral import ReferralCreate, ReferralResponse, ReferralUpdate
from app.services.referral import (
    create_referral_item,
    delete_referral_item,
    get_referral,
    list_referral,
    update_referral_item,
)

router = APIRouter(
    prefix="/referrals",
    tags=["Referrals"],
)


def _owner_filter(current_user):
    """Coordinators only ever see referrals they made."""
    return current_user.id if current_user.role == UserRole.COORDINATOR else None


@router.post("/", response_model=ReferralResponse, status_code=status.HTTP_201_CREATED)
def create_referral(payload: ReferralCreate, session: Session = Depends(get_session), current_user=Depends(require_roles_or_bot(UserRole.ADMIN))):
    try:
        return create_referral_item(session, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/", response_model=List[ReferralResponse])
def read_referrals(session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.COORDINATOR))):
    return list_referral(session, coordinator_user_id=_owner_filter(current_user))


@router.get("/{item_id}", response_model=ReferralResponse)
def read_referral(item_id: str, session: Session = Depends(get_session), current_user=Depends(require_roles(UserRole.ADMIN, UserRole.COORDINATOR))):
    item = get_referral(session, item_id)
    owner = _owner_filter(current_user)
    if item is None or (owner and item.get("coordinator_user_id") != owner):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ReferralResponse, dependencies=[Depends(require_roles(UserRole.ADMIN))])
def update_referral(item_id: str, payload: ReferralUpdate, session: Session = Depends(get_session)):
    item = update_referral_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles(UserRole.ADMIN))])
def delete_referral(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_referral_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

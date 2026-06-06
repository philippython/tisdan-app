from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import get_current_user, require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment import (
    create_payment_item,
    delete_payment_item,
    get_payment,
    list_payment,
    update_payment_item,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, session: Session = Depends(get_session)):
    return create_payment_item(session, payload)


@router.get("/", response_model=List[PaymentResponse])
def read_payments(session: Session = Depends(get_session)):
    return list_payment(session)


@router.get("/{item_id}", response_model=PaymentResponse)
def read_payment(item_id: str, session: Session = Depends(get_session)):
    item = get_payment(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=PaymentResponse)
def update_payment(
    item_id: str,
    payload: PaymentCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF)),
):
    item = update_payment_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
    item_id: str,
    session: Session = Depends(get_session),
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF)),
):
    deleted = delete_payment_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

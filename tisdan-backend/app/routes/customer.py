from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer import (
    create_customer_item,
    delete_customer_item,
    get_customer,
    list_customers,
    update_customer_item,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, session: Session = Depends(get_session)):
    return create_customer_item(session, payload)


@router.get("/", response_model=List[CustomerResponse])
def read_customers(session: Session = Depends(get_session)):
    return list_customers(session)


@router.get("/{item_id}", response_model=CustomerResponse)
def read_customer(item_id: str, session: Session = Depends(get_session)):
    item = get_customer(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=CustomerResponse, dependencies=[Depends(require_roles(UserRole.ADMIN))])
def update_customer(item_id: str, payload: CustomerCreate, session: Session = Depends(get_session)):
    item = update_customer_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles(UserRole.ADMIN))])
def delete_customer(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_customer_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
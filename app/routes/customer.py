from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.routes.dependencies import get_session
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer import (
    create_customer_item,
    get_customer,
    list_customers,
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

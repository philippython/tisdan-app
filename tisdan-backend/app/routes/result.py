from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.result import ResultCreate, ResultResponse
from app.services.result import (
    create_result_item,
    delete_result_item,
    get_result,
    list_result,
    update_result_item,
    get_results_by_customer,
    get_results_by_customer_name,
)

router = APIRouter(
    prefix="/results",
    tags=["Results"],
)


@router.post("/", response_model=ResultResponse, status_code=status.HTTP_201_CREATED)
def create_result(
    payload: ResultCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF, UserRole.DOCTOR)),
):
    return create_result_item(session, payload)


@router.get("/", response_model=List[ResultResponse])
def read_results(session: Session = Depends(get_session)):
    return list_result(session)


@router.get("/{item_id}", response_model=ResultResponse)
def read_result(item_id: str, session: Session = Depends(get_session)):
    item = get_result(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.get("/by-customer/{customer_id}", response_model=List[ResultResponse])
def read_results_by_customer(customer_id: str, session: Session = Depends(get_session)):
    return get_results_by_customer(session, customer_id)


@router.get("/by-customer-name/", response_model=List[ResultResponse])
def read_results_by_customer_name(name: str, session: Session = Depends(get_session)):
    return get_results_by_customer_name(session, name)


@router.put("/{item_id}", response_model=ResultResponse)
def update_result(
    item_id: str,
    payload: ResultCreate,
    session: Session = Depends(get_session),
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF, UserRole.DOCTOR)),
):
    item = update_result_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_result(
    item_id: str,
    session: Session = Depends(get_session),
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.STAFF, UserRole.DOCTOR)),
):
    deleted = delete_result_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

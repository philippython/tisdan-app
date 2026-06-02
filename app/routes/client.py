from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.client import ClientCreate, ClientResponse
from app.services.client import (
    create_client_item,
    delete_client_item,
    get_client,
    list_client,
    update_client_item,
)

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))],
)


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate, session: Session = Depends(get_session)):
    return create_client_item(session, payload)


@router.get("/", response_model=List[ClientResponse])
def read_clients(session: Session = Depends(get_session)):
    return list_client(session)


@router.get("/{item_id}", response_model=ClientResponse)
def read_client(item_id: str, session: Session = Depends(get_session)):
    item = get_client(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ClientResponse)
def update_client(item_id: str, payload: ClientCreate, session: Session = Depends(get_session)):
    item = update_client_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_client_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

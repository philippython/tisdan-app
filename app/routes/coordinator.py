from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.routes.dependencies import get_session
from app.schemas.coordinator import CoordinatorCreate, CoordinatorResponse
from app.services.coordinator import (
    create_coordinator_item,
    delete_coordinator_item,
    get_coordinator,
    list_coordinator,
    update_coordinator_item,
)

router = APIRouter(prefix="/coordinators", tags=["Coordinators"])


@router.post("/", response_model=CoordinatorResponse, status_code=status.HTTP_201_CREATED)
def create_coordinator(payload: CoordinatorCreate, session: Session = Depends(get_session)):
    return create_coordinator_item(session, payload)


@router.get("/", response_model=List[CoordinatorResponse])
def read_coordinators(session: Session = Depends(get_session)):
    return list_coordinator(session)


@router.get("/{item_id}", response_model=CoordinatorResponse)
def read_coordinator(item_id: str, session: Session = Depends(get_session)):
    item = get_coordinator(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=CoordinatorResponse)
def update_coordinator(item_id: str, payload: CoordinatorCreate, session: Session = Depends(get_session)):
    item = update_coordinator_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coordinator(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_coordinator_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

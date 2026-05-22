from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from routes.dependencies import get_session
from schemas.broadcast import BroadcastPersonalCreate, BroadcastPersonalResponse
from services.broadcast_personal import (
    create_broadcast_personal_item,
    delete_broadcast_personal_item,
    get_broadcast_personal,
    list_broadcast_personal,
    update_broadcast_personal_item,
)

router = APIRouter(prefix="/broadcasts/personal", tags=["BroadcastPersonal"])


@router.post("/", response_model=BroadcastPersonalResponse, status_code=status.HTTP_201_CREATED)
def create_broadcast_personal(payload: BroadcastPersonalCreate, session: Session = Depends(get_session)):
    return create_broadcast_personal_item(session, payload)


@router.get("/", response_model=List[BroadcastPersonalResponse])
def read_broadcast_personals(session: Session = Depends(get_session)):
    return list_broadcast_personal(session)


@router.get("/{item_id}", response_model=BroadcastPersonalResponse)
def read_broadcast_personal(item_id: str, session: Session = Depends(get_session)):
    item = get_broadcast_personal(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=BroadcastPersonalResponse)
def update_broadcast_personal(item_id: str, payload: BroadcastPersonalCreate, session: Session = Depends(get_session)):
    item = update_broadcast_personal_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_broadcast_personal(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_broadcast_personal_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.routes.dependencies import get_session
from app.schemas.broadcast import BroadcastGeneralCreate, BroadcastGeneralResponse
from app.services.broadcast_general import (
    create_broadcast_general_item,
    delete_broadcast_general_item,
    get_broadcast_general,
    list_broadcast_general,
    update_broadcast_general_item,
)

router = APIRouter(prefix="/broadcasts/general", tags=["BroadcastGeneral"])


@router.post("/", response_model=BroadcastGeneralResponse, status_code=status.HTTP_201_CREATED)
def create_broadcast_general(payload: BroadcastGeneralCreate, session: Session = Depends(get_session)):
    return create_broadcast_general_item(session, payload)


@router.get("/", response_model=List[BroadcastGeneralResponse])
def read_broadcast_generals(session: Session = Depends(get_session)):
    return list_broadcast_general(session)


@router.get("/{item_id}", response_model=BroadcastGeneralResponse)
def read_broadcast_general(item_id: str, session: Session = Depends(get_session)):
    item = get_broadcast_general(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=BroadcastGeneralResponse)
def update_broadcast_general(item_id: str, payload: BroadcastGeneralCreate, session: Session = Depends(get_session)):
    item = update_broadcast_general_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_broadcast_general(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_broadcast_general_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

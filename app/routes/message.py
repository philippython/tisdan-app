from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from routes.dependencies import get_session
from schemas.message import MessageCreate, MessageResponse
from services.message import (
    create_message_item,
    delete_message_item,
    get_message,
    list_message,
    update_message_item,
)

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(payload: MessageCreate, session: Session = Depends(get_session)):
    return create_message_item(session, payload)


@router.get("/", response_model=List[MessageResponse])
def read_messages(session: Session = Depends(get_session)):
    return list_message(session)


@router.get("/{item_id}", response_model=MessageResponse)
def read_message(item_id: str, session: Session = Depends(get_session)):
    item = get_message(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=MessageResponse)
def update_message(item_id: str, payload: MessageCreate, session: Session = Depends(get_session)):
    item = update_message_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_message_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

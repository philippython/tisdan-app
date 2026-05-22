from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from routes.dependencies import get_session
from schemas.chat import ChatCreate, ChatResponse
from services.chat import (
    create_chat_item,
    delete_chat_item,
    get_chat,
    list_chat,
    update_chat_item,
)

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(payload: ChatCreate, session: Session = Depends(get_session)):
    return create_chat_item(session, payload)


@router.get("/", response_model=List[ChatResponse])
def read_chats(session: Session = Depends(get_session)):
    return list_chat(session)


@router.get("/{item_id}", response_model=ChatResponse)
def read_chat(item_id: str, session: Session = Depends(get_session)):
    item = get_chat(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ChatResponse)
def update_chat(item_id: str, payload: ChatCreate, session: Session = Depends(get_session)):
    item = update_chat_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_chat_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

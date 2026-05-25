from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.routes.dependencies import get_session
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking import (
    create_booking_item,
    delete_booking_item,
    get_booking,
    list_booking,
    update_booking_item,
)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate, session: Session = Depends(get_session)):
    return create_booking_item(session, payload)


@router.get("/", response_model=List[BookingResponse])
def read_bookings(session: Session = Depends(get_session)):
    return list_booking(session)


@router.get("/{item_id}", response_model=BookingResponse)
def read_booking(item_id: str, session: Session = Depends(get_session)):
    item = get_booking(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=BookingResponse)
def update_booking(item_id: str, payload: BookingCreate, session: Session = Depends(get_session)):
    item = update_booking_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_booking_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

import json
from typing import List
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlmodel import Session
from app.dependencies.authentication import require_roles
from app.enums.role_enum import UserRole
from app.routes.dependencies import get_session
from app.schemas.payment import (
    PaymentCreate,
    PaymentInitializeRequest,
    PaymentInitializeResponse,
    PaymentResponse,
    PaymentUpdate,
)
from app.services.payment import (
    create_payment_item,
    delete_payment_item,
    get_payment,
    handle_paystack_event,
    initialize_payment,
    list_payment,
    update_payment_item,
    valid_paystack_signature,
    verify_payment,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)

staff_only = Depends(require_roles(UserRole.ADMIN, UserRole.STAFF))


@router.post("/paystack/webhook", include_in_schema=False)
async def paystack_webhook(
    request: Request,
    x_paystack_signature: str | None = Header(default=None),
    session: Session = Depends(get_session),
):
    """Paystack calls this when a transaction changes state. Set the URL in
    Paystack Dashboard → Settings → API Keys & Webhooks."""
    raw = await request.body()
    if not valid_paystack_signature(raw, x_paystack_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
    handle_paystack_event(session, json.loads(raw or b"{}"))
    return {"ok": True}


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED, dependencies=[staff_only])
def create_payment(payload: PaymentCreate, session: Session = Depends(get_session)):
    return create_payment_item(session, payload)


@router.post("/initialize/", response_model=PaymentInitializeResponse, status_code=status.HTTP_201_CREATED, dependencies=[staff_only])
def initialize_payment_route(payload: PaymentInitializeRequest, session: Session = Depends(get_session)):
    """Create a payment record, start a Paystack transaction, and WhatsApp
    the payment link to the payer. Used by the Bookings page's
    "send a payment link now" prompt."""
    return initialize_payment(session, payload)


@router.post("/verify/{reference}", response_model=PaymentResponse, dependencies=[staff_only])
def verify_payment_route(reference: str, session: Session = Depends(get_session)):
    """Re-check a payment's status with Paystack (fallback if a webhook was missed)."""
    try:
        item = verify_payment(session, reference)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return item


@router.get("/", response_model=List[PaymentResponse], dependencies=[staff_only])
def read_payments(session: Session = Depends(get_session)):
    return list_payment(session)


@router.get("/{item_id}", response_model=PaymentResponse, dependencies=[staff_only])
def read_payment(item_id: str, session: Session = Depends(get_session)):
    item = get_payment(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=PaymentResponse, dependencies=[staff_only])
def update_payment(item_id: str, payload: PaymentUpdate, session: Session = Depends(get_session)):
    item = update_payment_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[staff_only])
def delete_payment(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_payment_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None

from typing import Any
from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password
from app.repositories.user import (
    create_user,
    delete_user,
    get_user_by_email,
    get_user_by_id,
    get_all_user,
    update_user,
)
from app.repositories.staff import create_staff, delete_staff
from app.repositories.doctor import create_doctor, delete_doctor
from app.repositories.coordinator import create_coordinator, delete_coordinator
from app.enums.role_enum import UserRole
from app.models import Staff, Doctor, Coordinator


def list_user(session: Session):
    return get_all_user(session)


def get_user(session: Session, item_id: Any):
    return get_user_by_id(session, item_id)


def authenticate_user(session: Session, email: str, password: str):
    user = get_user_by_email(session, email)
    if user is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_user_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    if "password" in data:
        data["password"] = get_password_hash(data["password"])
    
    # Create the user first
    user = create_user(session, data)
    
    # Automatically create role-specific records
    role = data.get("role")
    if role == UserRole.STAFF:
        create_staff(session, {
            "user_id": user.id,
            "department": "General"
        })
    elif role == UserRole.DOCTOR:
        create_doctor(session, {
            "user_id": user.id,
            "specialization": "General",
            "license_number": f"LIC-{user.id.hex[:8].upper()}"
        })
    elif role == UserRole.COORDINATOR:
        create_coordinator(session, {
            "user_id": user.id,
            "referral_code": f"REF-{user.id.hex[:8].upper()}"
        })
    
    return user


def update_user_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    if "password" in data:
        data["password"] = get_password_hash(data["password"])
    return update_user(session, item_id, data)


def delete_user_item(session: Session, item_id: Any):
    """Delete user and associated role records."""
    user = get_user_by_id(session, item_id)
    if not user:
        return False
    
    # Delete role-specific records
    if user.role == UserRole.STAFF:
        stmt = select(Staff).where(Staff.user_id == user.id)
        staff = session.exec(stmt).first()
        if staff:
            delete_staff(session, staff.id)
    elif user.role == UserRole.DOCTOR:
        stmt = select(Doctor).where(Doctor.user_id == user.id)
        doctor = session.exec(stmt).first()
        if doctor:
            delete_doctor(session, doctor.id)
    elif user.role == UserRole.COORDINATOR:
        stmt = select(Coordinator).where(Coordinator.user_id == user.id)
        coordinator = session.exec(stmt).first()
        if coordinator:
            delete_coordinator(session, coordinator.id)
    
    # Delete the user
    return delete_user(session, item_id)

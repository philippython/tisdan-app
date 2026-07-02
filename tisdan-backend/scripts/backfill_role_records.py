#!/usr/bin/env python3
"""
Backfill script to create missing Staff, Doctor, and Coordinator records
for users that were created before the auto-creation feature was implemented.

Run this after updating the user service.
"""

import sys
import os
from sqlmodel import Session, select

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.database.db import engine
from app.database.setup import create_db_and_tables
from app.models import User, Staff, Doctor, Coordinator
from app.enums.role_enum import UserRole
from app.repositories.staff import create_staff
from app.repositories.doctor import create_doctor
from app.repositories.coordinator import create_coordinator


def backfill_role_records():
    """Create missing role-specific records for existing users."""
    
    # Ensure tables exist
    create_db_and_tables()
    
    with Session(engine) as session:
        # Find users with STAFF role but no Staff record
        staff_users = session.exec(
            select(User).where(User.role == UserRole.STAFF)
        ).all()
        
        staff_created = 0
        for user in staff_users:
            # Check if Staff record exists
            existing_staff = session.exec(
                select(Staff).where(Staff.user_id == user.id)
            ).first()
            
            if not existing_staff:
                try:
                    create_staff(session, {
                        "user_id": user.id,
                        "department": "General"
                    })
                    staff_created += 1
                    print(f"✓ Created Staff record for {user.full_name} ({user.email})")
                except Exception as e:
                    print(f"✗ Failed to create Staff record for {user.email}: {e}")
        
        if staff_created > 0:
            print(f"\nCreated {staff_created} Staff records\n")
        else:
            print("No new Staff records needed\n")
        
        # Find users with DOCTOR role but no Doctor record
        doctor_users = session.exec(
            select(User).where(User.role == UserRole.DOCTOR)
        ).all()
        
        doctor_created = 0
        for user in doctor_users:
            # Check if Doctor record exists
            existing_doctor = session.exec(
                select(Doctor).where(Doctor.user_id == user.id)
            ).first()
            
            if not existing_doctor:
                try:
                    create_doctor(session, {
                        "user_id": user.id,
                        "specialization": "General",
                        "license_number": f"LIC-{user.id.hex[:8].upper()}"
                    })
                    doctor_created += 1
                    print(f"✓ Created Doctor record for {user.full_name} ({user.email})")
                except Exception as e:
                    print(f"✗ Failed to create Doctor record for {user.email}: {e}")
        
        if doctor_created > 0:
            print(f"\nCreated {doctor_created} Doctor records\n")
        else:
            print("No new Doctor records needed\n")
        
        # Find users with COORDINATOR role but no Coordinator record
        coordinator_users = session.exec(
            select(User).where(User.role == UserRole.COORDINATOR)
        ).all()
        
        coordinator_created = 0
        for user in coordinator_users:
            # Check if Coordinator record exists
            existing_coordinator = session.exec(
                select(Coordinator).where(Coordinator.user_id == user.id)
            ).first()
            
            if not existing_coordinator:
                try:
                    create_coordinator(session, {
                        "user_id": user.id,
                        "referral_code": f"REF-{user.id.hex[:8].upper()}"
                    })
                    coordinator_created += 1
                    print(f"✓ Created Coordinator record for {user.full_name} ({user.email})")
                except Exception as e:
                    print(f"✗ Failed to create Coordinator record for {user.email}: {e}")
        
        if coordinator_created > 0:
            print(f"\nCreated {coordinator_created} Coordinator records\n")
        else:
            print("No new Coordinator records needed\n")
        
        total = staff_created + doctor_created + coordinator_created
        print(f"✓ Backfill complete! Created {total} total records.")


if __name__ == "__main__":
    backfill_role_records()

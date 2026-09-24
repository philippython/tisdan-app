#!/usr/bin/env python3
"""
Create (or reset the password of) an ADMIN user. Use this once on a fresh
deployment, since creating users through the API requires an admin login.

Usage:
    python scripts/create_admin.py admin@example.com "Full Name" 08012345678
    (you will be prompted for the password)
"""

import getpass
import os
import sys

from sqlmodel import Session, select

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.security import get_password_hash
from app.database.db import engine
from app.database.setup import create_db_and_tables
from app.enums.role_enum import UserRole
from app.models import User


def create_admin(email: str, full_name: str, phone_number: str, password: str) -> None:
    create_db_and_tables()

    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user:
            user.password = get_password_hash(password)
            user.role = UserRole.ADMIN
            print(f"OK: Updated existing user {email}: role=ADMIN, password reset")
        else:
            user = User(
                email=email,
                full_name=full_name,
                phone_number=phone_number,
                password=get_password_hash(password),
                role=UserRole.ADMIN,
            )
            print(f"OK: Created admin {email}")
        session.add(user)
        session.commit()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    password = os.environ.get("ADMIN_PASSWORD") or getpass.getpass("Password: ")
    if len(password) < 8:
        print("ERROR: Password must be at least 8 characters")
        sys.exit(1)
    create_admin(sys.argv[1], sys.argv[2], sys.argv[3], password)

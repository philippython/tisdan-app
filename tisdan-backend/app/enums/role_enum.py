from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    STAFF = "STAFF"
    CLIENT = "CLIENT"
    COORDINATOR = "COORDINATOR"
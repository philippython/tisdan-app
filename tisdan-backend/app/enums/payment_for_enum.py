from enum import Enum


class PaymentFor(str, Enum):
    TEST = "TEST"
    CONSULTATION = "CONSULTATION"
    REFERRAL = "REFERRAL"

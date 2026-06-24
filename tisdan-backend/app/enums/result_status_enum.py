from enum import Enum


class ResultStatus(str, Enum):
    PENDING = "PENDING"
    RELEASED = "RELEASED"
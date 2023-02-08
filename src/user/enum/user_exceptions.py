from enum import Enum


class UserExceptions(Enum):
    EMAIL_EXISTS = "Email address already exists"
    EMAIL_NOT_FOUND = "Email address not found"
    ID_NOT_FOUND = "ID not found"
    ACCOUNT_ACTIVATED = "User Account has already been activated"

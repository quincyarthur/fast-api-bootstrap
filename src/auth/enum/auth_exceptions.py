from enum import Enum


class AuthExceptions(Enum):
    WRONG_PASSWORD = "Password is incorrect"
    TOKEN_EXPIRED = "Token expired"
    INVALID_TOKEN = "Unable to validate token"

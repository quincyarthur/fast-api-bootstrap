from enum import Enum


class AuthExceptions(Enum):
    WRONG_PASSWORD = "Password is incorrect"
    TOKEN_EXPIRED = "Token expired"
    INVALID_TOKEN = "Unable to validate token"
    NOT_ACTIVATED = "Please activate your account before attemping to sign in"

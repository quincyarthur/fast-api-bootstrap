import os
from datetime import datetime, timedelta
from typing import Any
from jose import jwt
from dataclasses import dataclass

JWT_EXPIRE_MINUTES = 60 * 24 * 1  # 1 day
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]


@dataclass
class JWTToken:
    access_token: str


def create_access_token(subject: Any) -> JWTToken:
    expires_delta = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return JWTToken(access_token=encoded_jwt)


def decode_token(token: str) -> dict[str | Any]:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

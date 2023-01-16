from dataclasses import dataclass
from typing import Union, Any
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.jwt import decode_token
from src.auth.enum.auth_exceptions import AuthExceptions
from jose.exceptions import JWTError
from src.user.user_service import UserService, UserDTO

local_user_oauth = OAuth2PasswordBearer(tokenUrl="/signin", scheme_name="JWT")


@dataclass
class AuthService:
    def __init__(
        self,
        user_service: UserService = Depends(UserService),
        token: str = Depends(local_user_oauth),
    ) -> None:
        self.user_service = user_service
        self.token = token

    async def get_current_user(self) -> UserDTO:
        try:
            payload = decode_token(token=self.token)

            # invalidate token if exp is not found in payload
            exp = (
                datetime.now() - timedelta(minutes=1)
                if not payload.get("exp")
                else payload.get("exp")
            )

            if datetime.fromtimestamp(exp) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=AuthExceptions.TOKEN_EXPIRED.value,
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=AuthExceptions.INVALID_TOKEN.value,
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await self.user_service.find_by_id(id=payload.get("sub"))

        return await self.user_service.exclude_password(user=user)

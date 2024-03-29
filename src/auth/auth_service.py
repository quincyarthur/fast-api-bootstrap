from dataclasses import dataclass
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from utils.jwt import decode_token
from src.auth.enum.auth_exceptions import AuthExceptions
from jose.exceptions import JWTError
from src.user.user_service import UserService, UserDTO
from utils.jwt import create_access_token, JWTToken
from utils.password import Password
from src.user.interface.user_service_interface import IUserService
from src.auth.interface.auth_service_interface import IAuthService


@dataclass
class AuthService(IAuthService):
    user_service: IUserService = Depends(UserService)
    pwd: Password = Depends(Password)

    async def signin(self, email: str, password: str) -> JWTToken:
        user = await self.user_service.find_by_email(email=email)

        if not user.activated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthExceptions.NOT_ACTIVATED.value,
            )

        if not self.pwd.verify(
            plain_text_password=password, hashed_password=user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthExceptions.WRONG_PASSWORD.value,
            )

        return create_access_token(user.id)

    async def get_current_user(self, token: str) -> UserDTO:
        try:
            payload = decode_token(token=token)

            # invalidate token if exp is not found in payload
            exp = (
                (datetime.utcnow() - timedelta(minutes=1)).timestamp()
                if not payload.get("exp")
                else payload.get("exp")
            )

            if datetime.utcfromtimestamp(exp) < datetime.now():
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

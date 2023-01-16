from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.user.user_service import UserService
from utils.password import Password
from utils.jwt import create_access_token
from src.auth.enum.auth_exceptions import AuthExceptions

router = APIRouter()


@router.post("/signin", response_model=str)
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(UserService),
    pwd: Password = Depends(Password),
) -> str:
    user = await user_service.find_by_email(email=form_data.username)
    if not pwd.verify(
        plain_text_password=form_data.password, hashed_password=user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=AuthExceptions.WRONG_PASSWORD.value,
        )
    return create_access_token(user.id)

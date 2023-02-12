from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.user.user_service import UserService
from utils.password import Password
from utils.jwt import create_access_token, JWTToken
from starlette.requests import Request
from src.auth.config import oauth
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.dto.user_dto import UserDTO
from src.user.enum.user_origins import UserOrigins
from src.user.enum.user_exceptions import UserExceptions
from src.auth.auth_service import AuthService
from src.user.interface.user_service_interface import IUserService
from src.auth.interface.auth_service_interface import IAuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signin",
    response_model=JWTToken,
    summary="Signin",
    description="Accept email and password and return JWT Token if credentials are correct",
)
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: IAuthService = Depends(AuthService),
) -> str:
    return await auth_service.signin(
        email=form_data.username, password=form_data.password
    )


@router.get(
    "/google",
    response_model=JWTToken,
    summary="Google Auth Callback",
    description="Retrieves User Info from google, creates user if email does not exist and ultimately returns a JWT token",
)
async def google_auth(
    request: Request, user_service: IUserService = Depends(UserService)
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]
    user: UserDTO = None
    try:
        user = await user_service.find_by_email(email=user_info["email"])
    except HTTPException as e:
        if e.detail == UserExceptions.EMAIL_NOT_FOUND.value:
            create_user = CreateUserDTO(
                first_name=user_info["given_name"],
                last_name=user_info["family_name"],
                email=user_info["email"],
            )
            create_user.origin = UserOrigins.GOOGLE.value
            user = await user_service.add_user(create_user=create_user)
        else:
            raise e

    return create_access_token(subject=user.id)

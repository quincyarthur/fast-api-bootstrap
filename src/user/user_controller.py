from fastapi import APIRouter, Depends
from src.user.user_service import UserService, CreateUserDTO, UserDTO
from src.user.enum.user_origins import UserOrigins
from src.auth.auth_service import AuthService
from src.email.interface.email_interface import IEmail
from src.email.dto.email_dto import EmailDTO
from src.email.send_in_blue import SendInBlue, SIBEmailTemplates
import os
from utils.jwt import create_access_token
from utils.password import Password
from src.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.post("/", response_model=UserDTO, summary="Create user")
async def create_user(
    user: CreateUserDTO,
    user_service: UserService = Depends(UserService),
    response_model_exclude_none=True,
):
    user.origin = UserOrigins.LOCAL.value
    created_user = await user_service.add_user(create_user=user)
    return await user_service.exclude_password(user=created_user)


@router.get(
    "/me",
    response_model=UserDTO,
    summary="Get Current User",
    description="Find the current user based on the JWT token provided",
)
async def get_current_user(auth_service: AuthService = Depends(AuthService)):
    return await auth_service.get_current_user()


@router.post("/forgot-password", summary="Forgot Password")
async def forgot_password(
    email_address: str,
    user_service: UserService = Depends(UserService),
    email_service: IEmail = Depends(SendInBlue),
):
    user = await user_service.find_by_email(email=email_address)
    jwt = create_access_token(subject=user.id)
    reset_url = f"{os.environ['FRONTEND_URL']}/forgot-password?={jwt.access_token}"
    params = {"first_name": user.first_name.capitalize(), "reset_url": reset_url}
    email = EmailDTO(
        recipients=[user.email],
        template_id=SIBEmailTemplates.FORGOT_PASSWORD.value,
        params=params,
    )
    return await email_service.send(email=email)


@router.put("/password", summary="Update User Password")
async def update_password(
    user_password: str,
    current_user_id=Depends(JWTBearer()),
    user_service: UserService = Depends(UserService),
    pwd: Password = Depends(Password),
):
    user = await user_service.find_by_id(id=current_user_id)
    user.password = pwd.hash(password=user_password)
    return await user_service.update_password(user=user)

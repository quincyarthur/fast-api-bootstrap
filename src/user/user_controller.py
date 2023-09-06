from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from src.user.user_service import UserService, CreateUserDTO, UserDTO, UserExceptions
from src.user.enum.user_origins import UserOrigins
from src.auth.auth_service import AuthService
from src.email.interface.email_interface import IEmail
from src.email.dto.email_dto import EmailDTO
from src.email.send_in_blue import SendInBlue, SIBEmailTemplates
import os
from utils.jwt import create_access_token
from utils.password import Password
from src.user.interface.user_service_interface import IUserService
from src.auth.interface.auth_service_interface import IAuthService
from fastapi.security import OAuth2PasswordBearer

local_user_oauth = OAuth2PasswordBearer(tokenUrl="auth/signin")


router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.post("/", response_model=UserDTO, summary="Create user")
async def create_user(
    user: CreateUserDTO,
    background_tasks: BackgroundTasks,
    user_service: IUserService = Depends(UserService),
    response_model_exclude_none=True,
    email_service: IEmail = Depends(SendInBlue)
):
    user.origin = UserOrigins.LOCAL.value
    created_user = await user_service.add_user(create_user=user)
    created_user = await user_service.exclude_password(user=created_user)
    background_tasks.add_task(send_activation_email,user=created_user, email_service=email_service)
    return created_user


@router.get(
    "/me",
    response_model=UserDTO,
    summary="Get Current User",
    description="Find the current user based on the JWT token provided",
)
async def get_current_user(
    auth_service: IAuthService = Depends(AuthService),
    token: str = Depends(local_user_oauth),
):
    return await auth_service.get_current_user(token=token)


@router.post("/forgot-password", summary="Forgot Password")
async def forgot_password(
    email_address: str,
    user_service: IUserService = Depends(UserService),
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
    await email_service.send(email=email)


@router.put("/password", summary="Update User Password")
async def update_password(
    user_password: str,
    token: str = Depends(local_user_oauth),
    auth_service: IAuthService = Depends(AuthService),
    user_service: IUserService = Depends(UserService),
    pwd: Password = Depends(Password),
):
    current_user = await auth_service.get_current_user(token=token)
    current_user.password = pwd.hash(password=user_password)
    await user_service.update_password(user=current_user)


@router.put(
    "/activation",
    summary="Update User Activation Flag",
    description="Activate User using token sent in the activation email when the account was created",
)
async def update_activation_flag(
    token: str = Depends(local_user_oauth),
    auth_service: IAuthService = Depends(AuthService),
    user_service: IUserService = Depends(UserService),
):
    current_user = await auth_service.get_current_user(token=token)
    await user_service.update_activation_flag(user=current_user, activated=True)


@router.post("/resend-activation", summary="Resend User Activation Email")
async def resend_account_activation_email(
    email_address: str,
    user_service: IUserService = Depends(UserService),
    email_service: IEmail = Depends(SendInBlue),
):
    user = await user_service.find_by_email(email=email_address)
    await send_activation_email(user=user, email_service=email_service)


async def send_activation_email(user: UserDTO, email_service: IEmail) -> None:
    if user.activated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=UserExceptions.ACCOUNT_ACTIVATED.value,
        )
    jwt = create_access_token(subject=user.id)
    reset_url = f"{os.environ['FRONTEND_URL']}/activate?={jwt.access_token}"
    params = {"first_name": user.first_name.capitalize(), "reset_url": reset_url}
    email = EmailDTO(
        recipients=[user.email],
        template_id=SIBEmailTemplates.ACTIVATE_USER.value,
        params=params,
    )
    await email_service.send(email=email)

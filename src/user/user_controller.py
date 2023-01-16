from fastapi import APIRouter, Depends
from src.user.user_service import UserService, CreateUserDTO, UserDTO
from src.user.enum.user_origins import UserOrigins
from src.auth.auth_service import AuthService

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

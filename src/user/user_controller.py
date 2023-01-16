from fastapi import APIRouter, Depends
from src.user.user_service import UserService, CreateUserDTO, UserDTO
from src.user.enum.user_origins import UserOrigins

router = APIRouter()


@router.post("/user", response_model=UserDTO | None)
async def create_user(
    user: CreateUserDTO,
    user_service: UserService = Depends(UserService),
    response_model_exclude_none=True,
):
    user.origin = UserOrigins.LOCAL.value
    created_user = await user_service.add_user(create_user=user)
    return await user_service.exclude_password(user=created_user)

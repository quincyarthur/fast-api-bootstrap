from fastapi import APIRouter, Depends
from src.user.dto.user_dto import UserDTO
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.user_service import UserService

router = APIRouter()


@router.post("/user", response_model=UserDTO)
async def create_user(
    user: CreateUserDTO, user_service: UserService = Depends(UserService)
):
    return user_service.add_user(create_user=user)

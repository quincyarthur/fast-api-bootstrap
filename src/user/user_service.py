from dataclasses import dataclass
from src.user.user_repo import UserRepo, UserDTO, CreateUserDTO, AsyncSession
from fastapi import HTTPException, Depends, status
from src.user.enum.user_exceptions import UserExceptions


@dataclass
class UserService:
    def __init__(self, user_repo: UserRepo = Depends(UserRepo)):
        self.user_repo = user_repo

    async def add_user(self, create_user: CreateUserDTO) -> UserDTO:
        existing_user = await self.user_repo.find_by_email(email=create_user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=UserExceptions.EMAIL_EXISTS.value,
            )
        return await self.user_repo.add_user(create_user=create_user)

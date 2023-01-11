from dataclasses import dataclass
from src.user.user_repo import UserRepo, UserDTO, CreateUserDTO, AsyncSession
from fastapi import HTTPException, Depends
from src.user.enum.user_exceptions import UserExceptions


@dataclass
class UserService:
    def __init__(self, user_repo: UserRepo = Depends(UserRepo)):
        self.user_repo = user_repo

    async def add_user(self, create_user: CreateUserDTO) -> UserDTO:
        existing_user = await self.user_repo.find_by_email(email=create_user.email)
        if existing_user:
            raise HTTPException(
                status_code=400, detail=UserExceptions.EMAIL_EXISTS.value
            )
        print(f"Create User: {create_user}")
        return await self.user_repo.add_user(create_user=create_user)

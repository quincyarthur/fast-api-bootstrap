from dataclasses import dataclass
from src.user.user_repo import UserRepo, UserDTO, CreateUserDTO
from fastapi import HTTPException, Depends, status
from src.user.enum.user_exceptions import UserExceptions
from email_validator import validate_email, EmailNotValidError


@dataclass
class UserService:
    def __init__(self, user_repo: UserRepo = Depends(UserRepo)):
        self.user_repo = user_repo

    async def find_by_id(self, id: str) -> UserDTO:
        user = await self.user_repo.find_by_id(id=id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=UserExceptions.ID_NOT_FOUND.value,
            )
        return user

    async def find_by_email(self, email: str) -> UserDTO:
        user = await self.user_repo.find_by_email(email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=UserExceptions.EMAIL_NOT_FOUND.value,
            )
        return user

    async def add_user(self, create_user: CreateUserDTO) -> UserDTO:
        create_user.email = self.valiate_email(
            email=create_user.email, check_deliverability=True
        )
        existing_user = await self.user_repo.find_by_email(email=create_user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=UserExceptions.EMAIL_EXISTS.value,
            )
        return await self.user_repo.add_user(create_user=create_user)

    async def exclude_password(self, user: UserDTO) -> UserDTO:
        if user:
            user.password = None
        return user

    def valiate_email(self, email=str, check_deliverability: bool = False) -> str:
        try:
            validation = validate_email(
                email, check_deliverability=check_deliverability
            )
            validated_email = validation.email
            return validated_email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

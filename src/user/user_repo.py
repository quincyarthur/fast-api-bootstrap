from dataclasses import dataclass
from src.user.dto.user_dto import UserDTO
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.user_model import User
from db.config import get_session, AsyncSession
from sqlalchemy import select
from fastapi import Depends


@dataclass
class UserRepo:
    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        self.db_session = db

    async def find_by_email(self, email: str) -> UserDTO:
        user = await self.db_session.execute(select(User).where(User.email == email))
        return self.to_user_dto(user=user.first())

    async def add_user(self, create_user: CreateUserDTO) -> UserDTO:
        user = User(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            email=create_user.email,
            password=create_user.hashed_password,
        )
        user = self.db_session.add(user)
        self.db_session.commit()
        return self.to_user_dto(user=user)

    def to_user_dto(self, user: User) -> UserDTO:
        user_dto: UserDTO = None
        if user:
            user_dto = UserDTO(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                id=user.id,
            )
        return user_dto

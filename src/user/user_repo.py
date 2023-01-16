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

    async def find_by_id(self, id: str) -> UserDTO:
        user = await self.db_session.execute(select(User).where(User.id == id))
        user = user.scalar_one_or_none()
        return self.to_user_dto(user=user)

    async def find_by_email(self, email: str) -> UserDTO:
        user = await self.db_session.execute(select(User).where(User.email == email))
        user = user.scalar_one_or_none()
        return self.to_user_dto(user=user)

    async def add_user(self, create_user: CreateUserDTO) -> UserDTO:
        user = User(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            email=create_user.email,
            password=create_user.hashed_password,
            origin=create_user.origin,
            id=None,
        )
        self.db_session.add(user)
        await self.db_session.commit()
        return self.to_user_dto(user=user)

    def to_user_dto(self, user: User) -> UserDTO:
        user_dto: UserDTO = None

        if user:
            user_dto = UserDTO(**user.__dict__)

        return user_dto

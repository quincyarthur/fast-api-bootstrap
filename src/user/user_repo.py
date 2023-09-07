from dataclasses import dataclass
from src.user.dto.user_dto import UserDTO
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.user_model import User
from db.config import get_session, AsyncSession
from sqlalchemy import select, update, delete
from fastapi import Depends
from src.user.interface.user_service_repo_interface import IUserRepo
from typing import List
from datetime import datetime


@dataclass
class UserRepo(IUserRepo):
    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        self.db_session = db

    async def find_by_id(self, id: str) -> UserDTO:
        user = await self.db_session.execute(select(User).where(User.id == id))
        user = user.scalar_one_or_none()
        return self.to_user_dto(user=user)

    async def find_by_email(self, email: str) -> UserDTO:
        user = await self.db_session.execute(select(User).where(User.email == email))
        user = user.scalar()
        return self.to_user_dto(user=user)

    async def add_user(self, create_user: CreateUserDTO) -> UserDTO:
        user = User(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            email=create_user.email,
            password=create_user.hashed_password,
            origin=create_user.origin,
            activated=create_user.activated,
            id=None,
        )
        self.db_session.add(user)
        await self.db_session.commit()
        return self.to_user_dto(user=user)

    def to_user_dto(self, user: User) -> UserDTO:
        user_dto: UserDTO = None

        if user:
            user_dto = UserDTO(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                origin=user.origin,
                activated=user.activated,
                id=user.id,
            )

        return user_dto

    async def update_password(self, user: UserDTO) -> None:
        user = await self.db_session.execute(
            update(User).where(User.id == user.id).values(password=user.password)
        )
        return await self.db_session.commit()

    async def update_activation_flag(self, user: UserDTO, activated: bool) -> None:
        user = await self.db_session.execute(
            update(User).where(User.id == user.id).values(activated=activated)
        )
        return await self.db_session.commit()

    async def remove_expired_user_accounts(self, expiration: datetime) -> None:
        await self.db_session.execute(
            delete(User).where(
                User.activated == False and User.inserted_date <= expiration
            )
        )
        return await self.db_session.commit()

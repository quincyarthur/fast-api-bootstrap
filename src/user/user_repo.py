from dataclasses import dataclass
from src.user.dto.user_dto import UserDTO
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.user_model import User
from db.config import get_session
from sqlalchemy import select


@dataclass
class UserRepo:
    db_session = get_session()

    async def find_by_email(self, email: str) -> UserDTO:
        user = await self.db_session(select(User).where(User.email == email).limit(1))
        return self.to_user_dto(user=user)

    async def add_user(self, create_user: CreateUserDTO) -> UserDTO:
        user = User(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            email=create_user.email,
            password=create_user.hashed_password,
        )
        user = await self.db_session.add(user)
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

from abc import ABC, abstractclassmethod
from src.user.dto.user_dto import UserDTO
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.user_model import User
from typing import List
from datetime import datetime


class IUserRepo(ABC):
    @abstractclassmethod
    async def find_by_id(self, id: str) -> UserDTO:
        pass

    @abstractclassmethod
    async def find_by_email(self, email: str) -> UserDTO:
        pass

    @abstractclassmethod
    async def add_user(self, create_user: CreateUserDTO) -> UserDTO:
        pass

    @abstractclassmethod
    def to_user_dto(self, user: User) -> UserDTO:
        pass

    @abstractclassmethod
    async def update_password(self, user: UserDTO) -> None:
        pass

    @abstractclassmethod
    async def update_activation_flag(self, user: UserDTO, activated: bool) -> None:
        pass

    @abstractclassmethod
    async def remove_expired_user_accounts(self) -> None:
        pass

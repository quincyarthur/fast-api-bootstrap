from abc import ABC, abstractclassmethod, abstractproperty
from src.user.dto.user_dto import UserDTO
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.interface.user_service_repo import IUserRepo


class IUserService(ABC):
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
    async def exclude_password(self, user: UserDTO) -> UserDTO:
        pass

    @abstractclassmethod
    def valiate_email(self, email=str, check_deliverability: bool = False) -> str:
        pass

    @abstractclassmethod
    async def update_password(self, user: UserDTO) -> None:
        pass

    @abstractclassmethod
    async def update_activation_flag(self, user: UserDTO, activated: bool) -> None:
        pass

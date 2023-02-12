from abc import ABC, abstractclassmethod
from utils.jwt import JWTToken
from src.user.dto.user_dto import UserDTO


class IAuthService(ABC):
    @abstractclassmethod
    async def signin(self, email: str, password: str) -> JWTToken:
        pass

    @abstractclassmethod
    async def get_current_user(self) -> UserDTO:
        pass

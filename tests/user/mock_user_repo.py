from dataclasses import dataclass
from src.user.interface.user_service_repo_interface import IUserRepo
from src.user.dto.user_dto import UserDTO
from src.user.dto.create_user_dto import CreateUserDTO
from src.user.user_model import User
from src.user.enum.user_origins import UserOrigins


users = [
    UserDTO(
        first_name="John",
        last_name="Doe",
        email="johndoe@gmail.com",
        origin=UserOrigins.LOCAL.value,
        activated=False,
        password="secret",
        id=1,
    )
]


@dataclass
class MockUserRepo(IUserRepo):
    async def find_by_id(self, id: str) -> UserDTO:
        if id == 1:
            return users[0]
        else:
            return None

    async def find_by_email(self, email: str) -> UserDTO:
        if email == "johndoe@gmail.com":
            return users[0]
        else:
            return None

    async def add_user(self, create_user: CreateUserDTO) -> UserDTO:
        pass

    def to_user_dto(self, user: User) -> UserDTO:
        pass

    async def update_password(self, user: UserDTO) -> None:
        pass

    async def update_activation_flag(self, user: UserDTO, activated: bool) -> None:
        pass

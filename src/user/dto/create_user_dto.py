from dataclasses import dataclass
from src.user.dto.user_dto import UserDTO
from utils.password import Password


@dataclass
class CreateUserDTO(UserDTO):
    password: str

    def __post_init__(self) -> None:
        self.hashed_password = Password().hash(self.password)

from dataclasses import dataclass
from utils.password import Password


@dataclass
class CreateUserDTO:
    first_name: str
    last_name: str
    email: str
    password: str

    def __post_init__(self) -> None:
        self.hashed_password = Password().hash(self.password)

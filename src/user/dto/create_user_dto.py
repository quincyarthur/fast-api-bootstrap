from dataclasses import dataclass
from utils.password import Password
from typing import Optional


@dataclass
class CreateUserDTO:
    first_name: str
    last_name: str
    email: str
    password: str
    origin: Optional[str] = None

    def __post_init__(self) -> None:
        self.hashed_password = Password().hash(self.password)

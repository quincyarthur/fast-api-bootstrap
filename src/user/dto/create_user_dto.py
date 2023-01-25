from dataclasses import dataclass
from utils.password import Password
from typing import Optional


@dataclass
class CreateUserDTO:
    first_name: str
    last_name: str
    email: str
    password: Optional[str] = None
    origin: Optional[str] = None

    def __post_init__(self) -> None:
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        self.email = self.email.lower()
        self.hashed_password = Password().hash(self.password)

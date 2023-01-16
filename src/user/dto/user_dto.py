from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class UserDTO:
    first_name: str
    last_name: str
    email: str
    origin: str
    password: Optional[str] = None
    id: Optional[UUID] = None

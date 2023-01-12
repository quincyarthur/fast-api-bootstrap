from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class UserDTO:
    first_name: str
    last_name: str
    email: str
    id: Optional[UUID]

from dataclasses import dataclass
from typing import Optional


@dataclass
class UserDTO:
    first_name: str
    last_name: str
    email: str
    id: Optional[str]

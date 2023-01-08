from dataclasses import dataclass
from typing import Optional
import uuid


@dataclass
class UserDTO:
    first_name: str
    last_name: str
    email: str
    id: Optional[uuid.uuid4]

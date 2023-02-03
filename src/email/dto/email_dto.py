from typing import List, Optional
from dataclasses import dataclass


@dataclass
class EmailDTO:
    recipients: List[str]
    template_id: int
    params: dict
    sender: Optional[str] = None

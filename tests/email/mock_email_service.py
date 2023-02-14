from dataclasses import dataclass
from src.email.interface.email_interface import IEmail
from src.email.dto.email_dto import EmailDTO


@dataclass
class MockEmailService(IEmail):
    async def send(self, email: EmailDTO) -> None:
        pass

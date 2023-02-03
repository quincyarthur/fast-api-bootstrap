from abc import ABC, abstractmethod
from src.email.dto.email_dto import EmailDTO


class IEmail(ABC):
    @abstractmethod
    async def send(self, email: EmailDTO) -> None:
        pass

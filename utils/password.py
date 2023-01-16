from dataclasses import dataclass
from passlib.context import CryptContext


@dataclass
class Password:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify(self, plain_text_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_text_password, hashed_password)

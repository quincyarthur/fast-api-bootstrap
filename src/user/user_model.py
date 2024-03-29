from db.config import Base
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=True)
    origin = Column(String, nullable=False)
    activated = Column(Boolean, nullable=False, default=False)
    inserted_date = Column(DateTime, nullable=False, default=datetime.utcnow())

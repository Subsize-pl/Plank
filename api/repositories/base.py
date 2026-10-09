"""Shared declarative base for future ORM models."""
import uuid
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    @declared_attr
    def __init__(self):                     #TODO переписать нормально
        self.id : Mapped[UUID] = mapped_column(uuid.UUID(), primary_key=True)

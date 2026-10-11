"""Shared declarative base for future ORM models."""
from datetime import datetime
from uuid import UUID

from sqlalchemy import Uuid, DateTime, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        on_update=func.now(),
    )


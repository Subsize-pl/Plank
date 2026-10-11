from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


# TODO don't forget about limits
class User(Base):
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    boards: Mapped[list["Board"]] = relationship(
        back_populates="owner",
    )


class Board(Base):
    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    board_name: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        back_populates="boards",
    )

    columns: Mapped[list["Column"]] = relationship(
        back_populates="board",
    )

    __table_args__ = (UniqueConstraint("owner_id", "board_name"),)


class Column(Base):
    board_id: Mapped[UUID] = mapped_column(
        ForeignKey("boards.id"),
        nullable=False,
    )

    column_name: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )

    rank: Mapped[str] = mapped_column(
        Text(collation="C"),
        nullable=False,
    )

    board: Mapped["Board"] = relationship(
        back_populates="columns",
    )

    cards: Mapped[list["Card"]] = relationship(
        back_populates="column",
    )

    __table_args__ = (
        Index("ix_columns_board_id_rank", "board_id", "rank"),
        UniqueConstraint("board_id", "column_name"),
    )


class Card(Base):
    column_id: Mapped[UUID] = mapped_column(
        ForeignKey("columns.id", ondelete="RESTRICT"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text(),
        nullable=True,
    )

    rank: Mapped[str] = mapped_column(
        Text(collation="C"),
        nullable=False,
    )

    version: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
        server_default=text("1"),
    )

    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    column: Mapped["Column"] = relationship(
        back_populates="cards",
    )

    __table_args__ = (
        Index("ix_cards_column_id_rank", "column_id", "rank"),
        Index(
            "ix_cards_active_column_id_rank",
            "column_id",
            "rank",
            postgresql_where=text("archived_at IS NULL"),
        ),
    )

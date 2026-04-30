from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities import User, UserMeta
from .base import Base

if TYPE_CHECKING:
    from .card import CardORM


class UserORM(Base):
    """ORM для пользователя."""

    __tablename__ = 'users'

    login: Mapped[str] = mapped_column(
        primary_key=True,
        unique=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    avatar_path: Mapped[str] = mapped_column(nullable=False)
    time_block: Mapped[int] = mapped_column(nullable=False)
    salt: Mapped[bytes] = mapped_column(nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)

    cards: Mapped[list[CardORM]] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan'
    )

    def to_item(self):
        return User(
            UserMeta(
                self.name,
                Path(self.avatar_path),
                self.time_block,
                self.salt
            ),
            self.login,
            self.password
        )

    def __repr__(self) -> str:
        return ("<UserORM("
                f"login={self.login!r}, "
                f"name={self.name!r}, "
                f"avatar_path={self.avatar_path!r}, "
                f"time_block={self.time_block!r}"
                ")>")

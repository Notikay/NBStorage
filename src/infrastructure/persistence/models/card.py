from __future__ import annotations

from uuid import UUID
from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities import Card, MetaData
from .base import Base

if TYPE_CHECKING:
    from .user import UserORM


class CardORM(Base):
    """ORM для карточки пользователя."""

    __tablename__ = 'cards'

    user_login: Mapped[str] = mapped_column(
        ForeignKey('users.login', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        index=True
    )
    card_id: Mapped[UUID] = mapped_column(
        primary_key=True
    )
    title: Mapped[str] = mapped_column(nullable=False)
    icon_path: Mapped[str] = mapped_column(nullable=False)
    key: Mapped[bytes] = mapped_column(nullable=False)
    username: Mapped[bytes | None] = mapped_column(nullable=True)
    email: Mapped[bytes | None] = mapped_column(nullable=True)
    password: Mapped[bytes | None] = mapped_column(nullable=True)
    url: Mapped[bytes | None] = mapped_column(nullable=True)
    description: Mapped[bytes | None] = mapped_column(nullable=True)

    owner: Mapped[UserORM] = relationship(back_populates='cards')

    def to_item(self):
        return Card(
            MetaData(
                self.title,
                Path(self.icon_path),
                self.user_login,
                self.key
            ),
            self.username,
            self.email,
            self.password,
            self.url,
            self.description
        )

    def __repr__(self) -> str:
        return ("<CardORM("
                f"card_id={self.card_id!r}, "
                f"user_login={self.user_login!r}, "
                f"title={self.title!r}, "
                f"icon_path={self.icon_path!r}, "
                f"username={self.username!r}, "
                f"email={self.email!r}, "
                f"password={self.password!r}, "
                f"url={self.url!r}, "
                f"description={self.description!r}"
                ")>")

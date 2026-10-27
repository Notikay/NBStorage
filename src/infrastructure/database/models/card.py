from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.card import Card, CardMeta

from .base import Base
from .types import (
    CardModelCardIDType,
    CardModelIconKeyType,
    CardModelKeyType,
    CardModelParamType,
    CardModelTitleType,
    CardModelUserIDType,
)

if TYPE_CHECKING:
    from .user import UserModel


class CardModel(Base):
    __tablename__ = 'cards'

    card_id: Mapped[CardModelCardIDType] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[CardModelUserIDType] = mapped_column(
        ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'),
        index=True
    )
    title: Mapped[CardModelTitleType] = mapped_column(nullable=False)
    icon_key: Mapped[CardModelIconKeyType] = mapped_column(nullable=True)
    key: Mapped[CardModelKeyType] = mapped_column(nullable=False)
    username: Mapped[CardModelParamType] = mapped_column(nullable=True)
    email: Mapped[CardModelParamType] = mapped_column(nullable=True)
    password: Mapped[CardModelParamType] = mapped_column(nullable=True)
    url: Mapped[CardModelParamType] = mapped_column(nullable=True)
    description: Mapped[CardModelParamType] = mapped_column(nullable=True)

    user: Mapped[UserModel] = relationship(back_populates='cards')

    def to_item(self) -> Card:
        return Card(
            CardMeta(self.title, self.icon_key, self.user_id,  self.key),
            self.username,
            self.email,
            self.password,
            self.url,
            self.description
        )

    def __repr__(self) -> str:
        return ("<CardORM("
                f"card_id={self.card_id!r}, "
                f"user_id={self.user_id!r}, "
                f"title={self.title!r}, "
                f"icon_key={self.icon_key!r}"
                ")>")

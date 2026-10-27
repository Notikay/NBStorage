from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.user import User, UserMeta

from .base import Base
from .types import (
    UserModelAvatarKeyType,
    UserModelIDType,
    UserModelLoginType,
    UserModelNameType,
    UserModelPasswordType,
    UserModelSaltType,
    UserModelTimeBlockType,
)

if TYPE_CHECKING:
    from .card import CardModel


class UserModel(Base):
    __tablename__ = 'users'

    user_id: Mapped[UserModelIDType] = mapped_column(primary_key=True, unique=True)
    name: Mapped[UserModelNameType] = mapped_column(nullable=False)
    avatar_key: Mapped[UserModelAvatarKeyType] = mapped_column(nullable=True)
    time_block: Mapped[UserModelTimeBlockType] = mapped_column(nullable=False)
    salt: Mapped[UserModelSaltType] = mapped_column(nullable=False)
    login: Mapped[UserModelLoginType] = mapped_column(nullable=False, unique=True)
    password: Mapped[UserModelPasswordType] = mapped_column(nullable=False)

    cards: Mapped[list[CardModel]] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )

    def to_item(self) -> User:
        return User(
            UserMeta(self.name, self.avatar_key, self.time_block, self.salt),
            self.login,
            self.password
        )

    def __repr__(self) -> str:
        return ("<UserORM("
                f"user_id={self.user_id!r}, "
                f"name={self.name!r}, "
                f"avatar_key={self.avatar_key!r}, "
                f"time_block={self.time_block!r}"
                f"login={self.login!r}"
                ")>")

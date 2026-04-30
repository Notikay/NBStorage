from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from base import AbstractEntity

if TYPE_CHECKING:
    from .types import (
        UserMetaSaltType,
        UserMetaNameType,
        UserMetaUpdNameType,
        UserMetaAvatarPathType,
        UserMetaUpdAvatarPathType,
        UserMetaTimeBlockType,
        UserMetaUpdTimeBlockType,
        UserLoginType,
        UserPasswordType
    )


@dataclass
class UserMetaEntityInterface(AbstractEntity):
    """Интерфейс сущности метаданных пользователя."""

    @property
    @abstractmethod
    def salt(self) -> UserMetaSaltType:
        pass

    @property
    @abstractmethod
    def name(self) -> UserMetaNameType:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: UserMetaUpdNameType) -> None:
        pass

    @property
    @abstractmethod
    def avatar_path(self) -> UserMetaAvatarPathType:
        pass

    @avatar_path.setter
    @abstractmethod
    def avatar_path(self, value: UserMetaUpdAvatarPathType) -> None:
        pass

    @property
    @abstractmethod
    def time_block(self) -> UserMetaTimeBlockType:
        pass

    @time_block.setter
    @abstractmethod
    def time_block(self, value: UserMetaUpdTimeBlockType) -> None:
        pass


@dataclass
class UserEntityInterface(AbstractEntity):
    """Интерфейс сущности пользователя."""

    @property
    @abstractmethod
    def meta(self) -> UserMetaEntityInterface:
        pass

    @property
    @abstractmethod
    def login(self) -> UserLoginType:
        pass

    @property
    @abstractmethod
    def password(self) -> UserPasswordType:
        pass

    @password.setter
    @abstractmethod
    def password(self, value: UserPasswordType) -> None:
        pass

    @abstractmethod
    def hash_password(self) -> None:
        pass

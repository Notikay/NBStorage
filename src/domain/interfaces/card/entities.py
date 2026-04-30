from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from base import AbstractEntity

if TYPE_CHECKING:
    from .types import (
        CardMetaUserLoginType,
        CardMetaKeyType,
        CardMetaCardIDType,
        CardMetaTitleType,
        CardMetaUpdTitleType,
        CardMetaIconPathType,
        CardMetaUpdIconPathType,
        CardParamType,
        CardUpdParamType
    )


@dataclass
class CardMetaEntityInterface(AbstractEntity):
    """Интерфейс сущности метаданных карточки пользователя."""

    @property
    @abstractmethod
    def user_login(self) -> CardMetaUserLoginType:
        pass

    @property
    @abstractmethod
    def key(self) -> CardMetaKeyType:
        pass

    @property
    @abstractmethod
    def card_id(self) -> CardMetaCardIDType:
        pass

    @property
    @abstractmethod
    def title(self) -> CardMetaTitleType:
        pass

    @title.setter
    @abstractmethod
    def title(self, value: CardMetaUpdTitleType) -> None:
        pass

    @property
    @abstractmethod
    def icon_path(self) -> CardMetaIconPathType:
        pass

    @icon_path.setter
    @abstractmethod
    def icon_path(self, value: CardMetaUpdIconPathType) -> None:
        pass

    @abstractmethod
    def generate_card_id(self) -> None:
        pass


@dataclass
class CardEntityInterface(AbstractEntity):
    """Интерфейс сущности карточки пользователя."""

    @property
    @abstractmethod
    def meta(self) -> CardMetaEntityInterface:
        pass

    @property
    @abstractmethod
    def username(self) -> CardParamType:
        pass

    @username.setter
    @abstractmethod
    def username(self, value: CardUpdParamType) -> None:
        pass

    @property
    @abstractmethod
    def email(self) -> CardParamType:
        pass

    @email.setter
    @abstractmethod
    def email(self, value: CardUpdParamType) -> None:
        pass

    @property
    @abstractmethod
    def password(self) -> CardParamType:
        pass

    @password.setter
    def password(self, value: CardUpdParamType) -> None:
        pass

    @property
    @abstractmethod
    def url(self) -> CardParamType:
        pass

    @url.setter
    @abstractmethod
    def url(self, value: CardUpdParamType) -> None:
        pass

    @property
    @abstractmethod
    def description(self) -> CardParamType:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: CardUpdParamType) -> None:
        pass

    @abstractmethod
    def encrypt(self) -> None:
        pass

    @abstractmethod
    def decrypt(self) -> None:
        pass

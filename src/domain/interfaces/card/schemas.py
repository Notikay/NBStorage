from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from base import AbstractSchema
from .types import (
    CardMetaTitleType,
    CardMetaIconPathType,
    CardParamType,
    CardUpdParamType,
    CardMetaUpdTitleType,
    CardMetaUpdIconPathType
)

if TYPE_CHECKING:
    from .types import CardMetaUserLoginType, CardMetaCardIDType


class AbstractUserLoginValidate(ABC):
    """Абстрактный класс валидации логина пользователя."""

    @abstractmethod
    def validate_user_login(
            self,
            user_login: CardMetaUserLoginType
    ) -> CardMetaUserLoginType:
        pass


class AbstractCardIDValidate(ABC):
    """Абстрактный класс валидации ID карточки пользователя."""

    @abstractmethod
    def validate_card_id(
            self,
            card_id: CardMetaCardIDType
    ) -> CardMetaCardIDType:
        pass


class AbstractMetaValidate[
    T: CardMetaTitleType | CardMetaUpdTitleType,
    U: CardMetaIconPathType | CardMetaUpdIconPathType
](ABC):
    """Абстрактный класс валидации метаданных карточки пользователя."""

    @abstractmethod
    def validate_title(self, title: T) -> T:
        pass

    @abstractmethod
    def validate_icon_path(self, icon_path: U) -> U:
        pass


class AbstractDataValidate[T: CardParamType | CardUpdParamType](ABC):
    """Абстрактный класс валидации данных карточки пользователя."""

    @abstractmethod
    def validate_username(self, username: T) -> T:
        pass

    @abstractmethod
    def validate_email(self, email: T) -> T:
        pass

    @abstractmethod
    def validate_password(self, password: T) -> T:
        pass

    @abstractmethod
    def validate_url(self, url: T) -> T:
        pass

    @abstractmethod
    def validate_description(self, description: T) -> T:
        pass


class BaseCardSchemaInterface(AbstractSchema, ABC):
    """Базовый интерфейс схемы карточки пользователя."""
    ...


class ChooseCardSchemaInterface(
    AbstractUserLoginValidate,
    AbstractCardIDValidate,
    BaseCardSchemaInterface,
    ABC
):
    """Интерфейс схемы при получении карточки пользователя."""
    ...


class ChooseAllCardsSchemaInterface(
    AbstractUserLoginValidate,
    BaseCardSchemaInterface,
    ABC
):
    """Интерфейс схемы при получении всех карточек пользователя."""
    ...


class CreateCardSchemaInterface(
    AbstractUserLoginValidate,
    AbstractCardIDValidate,
    AbstractMetaValidate[CardMetaTitleType, CardMetaIconPathType],
    AbstractDataValidate[CardParamType],
    BaseCardSchemaInterface,
    ABC
):
    """Интерфейс схемы при создании карточки пользователя."""
    ...


class DeleteCardSchemaInterface(
    AbstractUserLoginValidate,
    AbstractCardIDValidate,
    BaseCardSchemaInterface,
    ABC
):
    """Интерфейс схемы при удалении карточки пользователя."""
    ...


class DeleteAllCardsSchemaInterface(
    AbstractUserLoginValidate,
    BaseCardSchemaInterface,
    ABC
):
    """Интерфейс схемы при удалении всех карточек пользователя."""
    ...


class UpdateCardSchemaInterface(
    AbstractUserLoginValidate,
    AbstractCardIDValidate,
    AbstractDataValidate[CardUpdParamType],
    BaseCardSchemaInterface,
    ABC
):
    """Интерфейс схемы при обновлении карточки пользователя."""
    ...


class UpdateCardMetaSchemaInterface(
    AbstractUserLoginValidate,
    AbstractCardIDValidate,
    AbstractMetaValidate[CardMetaUpdTitleType, CardMetaUpdIconPathType],
    BaseCardSchemaInterface,
    ABC
):
    """
    Интерфейс схемы при обновлении метаданных карточки пользователя.
    """
    ...

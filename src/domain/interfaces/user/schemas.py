from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from base import AbstractSchema
from .types import (
    UserMetaNameType,
    UserMetaAvatarPathType,
    UserMetaTimeBlockType,
    UserMetaUpdNameType,
    UserMetaUpdAvatarPathType,
    UserMetaUpdTimeBlockType
)

if TYPE_CHECKING:
    from .types import UserLoginType, UserPasswordType


class AbstractLoginValidate(ABC):
    """Абстрактный класс валидации логина."""

    @abstractmethod
    def validate_login(self, login: UserLoginType) -> UserLoginType:
        pass


class AbstractPasswordValidate(ABC):
    """Абстрактный класс валидации пароля пользователя."""

    @abstractmethod
    def validate_password(self, password: UserPasswordType):
        pass


class AbstractMetaValidate[
    T: UserMetaNameType | UserMetaUpdNameType,
    U: UserMetaAvatarPathType | UserMetaUpdAvatarPathType,
    V: UserMetaTimeBlockType | UserMetaUpdTimeBlockType
](ABC):
    """Абстрактный класс валидации метаданных пользователя."""

    @abstractmethod
    def validate_name(self, name: T) -> T:
        pass

    @abstractmethod
    def validate_avatar_path(self, avatar_path: U) -> U:
        pass

    @abstractmethod
    def validate_time_block(self, time_block: V) -> V:
        pass


class BaseUserSchemaInterface(AbstractSchema, ABC):
    """Базовый интерфейс схемы пользователя."""
    ...


class ChooseUserSchemaInterface(
    AbstractLoginValidate,
    BaseUserSchemaInterface,
    ABC
):
    """Абстрактный класс схемы при получении пользователя."""
    ...


class CreateUserSchemaInterface(
    AbstractLoginValidate,
    AbstractMetaValidate[
        UserMetaNameType,
        UserMetaAvatarPathType,
        UserMetaTimeBlockType
    ],
    AbstractPasswordValidate,
    BaseUserSchemaInterface,
    ABC
):
    """Абстрактный класс схемы при создании пользователя."""
    ...


class DeleteUserSchemaInterface(
    AbstractLoginValidate,
    BaseUserSchemaInterface,
    ABC
):
    """Абстрактный класс схемы при удалении пользователя."""
    ...


class UpdateUserMetaSchemaInterface(
    AbstractLoginValidate,
    AbstractMetaValidate[
        UserMetaUpdNameType,
        UserMetaUpdAvatarPathType,
        UserMetaUpdTimeBlockType
    ],
    BaseUserSchemaInterface,
    ABC
):
    """
    Абстрактный класс схемы при обновлении метаданных пользователя.
    """
    ...


class ChangeUserPasswordSchemaInterface(
    AbstractLoginValidate,
    AbstractPasswordValidate,
    BaseUserSchemaInterface,
    ABC
):
    """Абстрактный класс схемы при изменении пароля пользователя."""
    ...

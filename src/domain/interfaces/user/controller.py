from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any

from base import AbstractController
from .schemas import (
    ChooseUserSchemaInterface,
    CreateUserSchemaInterface,
    DeleteUserSchemaInterface,
    UpdateUserMetaSchemaInterface,
    ChangeUserPasswordSchemaInterface
)
from .view import UserViewInterface

if TYPE_CHECKING:
    from .schemas import BaseUserSchemaInterface


class BaseUserControllerInterface[T: BaseUserSchemaInterface](
    AbstractController[T, UserViewInterface],
    ABC
):
    """Базовый интерфейс контроллера пользователя."""
    ...


class ChooseUserControllerInterface(
    BaseUserControllerInterface[ChooseUserSchemaInterface],
    ABC
):
    """Интерфейс контроллера получения пользователя."""
    ...


class ChooseAllUsersControllerInterface(BaseUserControllerInterface[Any], ABC):
    """Интерфейс контроллера получения всех пользователей."""
    ...


class CreateUserControllerInterface(
    BaseUserControllerInterface[CreateUserSchemaInterface],
    ABC
):
    """Интерфейс контроллера создания пользователя."""
    ...


class DeleteUserControllerInterface(
    BaseUserControllerInterface[DeleteUserSchemaInterface],
    ABC
):
    """Интерфейс контроллера удаления пользователя."""
    ...


class DeleteAllUsersControllerInterface(BaseUserControllerInterface[Any], ABC):
    """Интерфейс контроллера удаления всех пользователей."""
    ...


class UpdateUserMetaControllerInterface(
    BaseUserControllerInterface[UpdateUserMetaSchemaInterface],
    ABC
):
    """Интерфейс контроллера обновления метаданных пользователя."""
    ...


class ChangeUserPasswordControllerInterface(
    BaseUserControllerInterface[ChangeUserPasswordSchemaInterface],
    ABC
):
    """Интерфейс контроллера изменения пароля пользователя."""
    ...

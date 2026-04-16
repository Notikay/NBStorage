from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from domain.interfaces import AbstractUseCase

if TYPE_CHECKING:
    from domain.interfaces.base.base_types import MapType
    from .entities import UserEntityInterface
    from .user_types import (
        UserLoginType,
        UserPasswordType,
        SettingsNameType,
        SettingsAvatarPathType,
        SettingsTimeBlockType,
        SettingsUpdNameType,
        SettingsUpdAvatarPathType,
        SettingsUpdTimeBlockType
    )


class ChooseUserUseCaseInterface[T: UserEntityInterface[MapType]](
    AbstractUseCase,
    ABC
):
    """Интерфейс бизнес-логики получения пользователя."""

    @override
    @abstractmethod
    def execute(self, login: UserLoginType) -> T:
        pass


class ChooseAllUsersUseCaseInterface[T: UserEntityInterface[MapType]](
    AbstractUseCase,
    ABC
):
    """Интерфейс бизнес-логики получения всех пользователей."""

    @override
    @abstractmethod
    def execute(self) -> list[T]:
        pass


class CreateUserUseCaseInterface[T: UserEntityInterface[MapType]](
    AbstractUseCase,
    ABC
):
    """Интерфейс бизнес-логики создания пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            login: UserLoginType,
            password: UserPasswordType,
            name: SettingsNameType,
            avatar_path: SettingsAvatarPathType,
            time_block: SettingsTimeBlockType
    ) -> T:
        pass


class DeleteUserUseCaseInterface(AbstractUseCase, ABC):
    """Интерфейс бизнес-логики удаления пользователя."""

    @override
    @abstractmethod
    def execute(self, login: UserLoginType) -> None:
        pass


class DeleteAllUsersUseCaseInterface(AbstractUseCase, ABC):
    """Интерфейс бизнес-логики удаления всех пользователей."""

    @override
    @abstractmethod
    def execute(self) -> None:
        pass


class UpdateSettingsUseCaseInterface[T: UserEntityInterface[MapType]](
    AbstractUseCase,
    ABC
):
    """Интерфейс бизнес-логики обновления настроек пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            login: UserLoginType,
            name: SettingsUpdNameType,
            avatar_path: SettingsUpdAvatarPathType,
            time_block: SettingsUpdTimeBlockType
    ) -> T:
        pass


class ChangeUserPasswordUseCaseInterface[T: UserEntityInterface[MapType]](
    AbstractUseCase,
    ABC
):
    """Интерфейс бизнес-логики смены пароля пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            login: UserLoginType,
            new_password: UserPasswordType
    ) -> T:
        pass

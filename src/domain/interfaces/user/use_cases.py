from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, override, Sequence, Any

from base import AbstractUseCase

if TYPE_CHECKING:
    from .entities import UserEntityInterface
    from .types import (
        UserLoginType,
        UserPasswordType,
        UserMetaNameType,
        UserMetaAvatarPathType,
        UserMetaTimeBlockType,
        UserMetaUpdNameType,
        UserMetaUpdAvatarPathType,
        UserMetaUpdTimeBlockType
    )


class ChooseUserUseCaseInterface[T: UserEntityInterface](AbstractUseCase[T]):
    """Интерфейс бизнес-логики получения пользователя."""

    @override
    @abstractmethod
    def execute(self, login: UserLoginType) -> T:
        pass


class ChooseAllUsersUseCaseInterface[T: UserEntityInterface](
    AbstractUseCase[T]
):
    """Интерфейс бизнес-логики получения всех пользователей."""

    @override
    @abstractmethod
    def execute(self) -> Sequence[T]:
        pass


class CreateUserUseCaseInterface[T: UserEntityInterface](AbstractUseCase[T]):
    """Интерфейс бизнес-логики создания пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            login: UserLoginType,
            password: UserPasswordType,
            name: UserMetaNameType,
            avatar_path: UserMetaAvatarPathType,
            time_block: UserMetaTimeBlockType
    ) -> T:
        pass


class DeleteUserUseCaseInterface(AbstractUseCase[Any]):
    """Интерфейс бизнес-логики удаления пользователя."""

    @override
    @abstractmethod
    def execute(self, login: UserLoginType) -> None:
        pass


class DeleteAllUsersUseCaseInterface(AbstractUseCase[Any]):
    """Интерфейс бизнес-логики удаления всех пользователей."""

    @override
    @abstractmethod
    def execute(self) -> None:
        pass


class UpdateUserMetaUseCaseInterface[T: UserEntityInterface](
    AbstractUseCase[T]
):
    """Интерфейс бизнес-логики обновления метаданных пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            login: UserLoginType,
            name: UserMetaUpdNameType,
            avatar_path: UserMetaUpdAvatarPathType,
            time_block: UserMetaUpdTimeBlockType
    ) -> T:
        pass


class ChangeUserPasswordUseCaseInterface[T: UserEntityInterface](
    AbstractUseCase[T]
):
    """Интерфейс бизнес-логики изменения пароля пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            login: UserLoginType,
            new_password: UserPasswordType
    ) -> T:
        pass

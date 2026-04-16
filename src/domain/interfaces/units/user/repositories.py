from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from domain.interfaces import AbstractRepository

if TYPE_CHECKING:
    from domain.interfaces.base.base_types import MapType
    from .entities import UserEntityInterface
    from .user_types import UserLoginType


class UserRepositoryInterface[T: UserEntityInterface[MapType]](
    AbstractRepository[T],
    ABC
):
    """Интерфейс репозитория хранилища пользователя."""

    @override
    @abstractmethod
    def get_item(self, login: UserLoginType) -> T | None:
        pass

    @override
    @abstractmethod
    def get_all_items(self) -> list[T]:
        pass

    @override
    @abstractmethod
    def del_item(self, login: UserLoginType) -> None:
        pass

    @override
    @abstractmethod
    def del_all_items(self) -> None:
        pass

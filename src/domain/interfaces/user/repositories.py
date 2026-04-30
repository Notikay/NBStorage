from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, override, Sequence

from base import AbstractRepository

if TYPE_CHECKING:
    from .entities import UserEntityInterface
    from .types import UserLoginType


class UserRepositoryInterface[T: UserEntityInterface](AbstractRepository[T]):
    """Интерфейс репозитория хранилища пользователя."""

    @override
    @abstractmethod
    def get_item(self, login: UserLoginType) -> T | None:
        pass

    @override
    @abstractmethod
    def get_all_items(self) -> Sequence[T]:
        pass

    @override
    @abstractmethod
    def del_item(self, login: UserLoginType) -> None:
        pass

    @override
    @abstractmethod
    def del_all_items(self) -> None:
        pass

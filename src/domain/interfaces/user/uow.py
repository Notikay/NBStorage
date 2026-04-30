from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from base import AbstractUnitOfWork

if TYPE_CHECKING:
    from .entities import UserEntityInterface
    from .repositories import UserRepositoryInterface


class UserUnitOfWorkInterface[T: UserEntityInterface](AbstractUnitOfWork):
    """Интерфейс управления транзакцией пользователя."""

    @property
    @abstractmethod
    def user_repos(self) -> UserRepositoryInterface[T]:
        pass

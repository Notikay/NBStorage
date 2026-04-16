from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from domain.interfaces import AbstractUnitOfWork

if TYPE_CHECKING:
    from domain.interfaces.base.base_types import MapType
    from . import UserRepositoryInterface, UserEntityInterface


class UserUnitOfWorkInterface[T: UserEntityInterface[MapType]](
    AbstractUnitOfWork,
    ABC
):
    """Менеджер состояния транзакции пользователя."""

    @property
    @abstractmethod
    def user_repos(self) -> UserRepositoryInterface[T]:
        pass

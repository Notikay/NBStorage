from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from base import AbstractUnitOfWork

if TYPE_CHECKING:
    from .entities import CardEntityInterface
    from .repositories import CardRepositoryInterface


class CardUnitOfWorkInterface[T: CardEntityInterface](AbstractUnitOfWork):
    """Интерфейс управления транзакцией карточки пользователя."""

    @property
    @abstractmethod
    def card_repos(self) -> CardRepositoryInterface[T]:
        pass

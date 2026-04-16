from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from domain.interfaces import AbstractUnitOfWork

if TYPE_CHECKING:
    from domain.interfaces.base.base_types import MapType
    from . import CardRepositoryInterface, CardEntityInterface


class CardUnitOfWorkInterface[T: CardEntityInterface[MapType]](
    AbstractUnitOfWork,
    ABC
):
    """Менеджер состояния транзакции карточки пользователя."""

    @property
    @abstractmethod
    def card_repos(self) -> CardRepositoryInterface[T]:
        pass

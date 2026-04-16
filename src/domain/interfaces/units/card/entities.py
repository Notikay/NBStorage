from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from domain.interfaces import AbstractEntity

if TYPE_CHECKING:
    from domain.interfaces.base.base_types import MapType


class CardEntityInterface[T: MapType](AbstractEntity[T], ABC):
    """Интерфейс сущности карточки пользователя."""

    @abstractmethod
    def encrypt(self) -> None:
        pass

    @abstractmethod
    def decrypt(self) -> None:
        pass

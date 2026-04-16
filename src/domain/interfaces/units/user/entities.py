from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from domain.interfaces import AbstractEntity

if TYPE_CHECKING:
    from domain.interfaces.base.base_types import MapType


class UserEntityInterface[T: MapType](AbstractEntity[T], ABC):
    """Интерфейс сущности пользователя."""

    @abstractmethod
    def hash_password(self) -> None:
        pass

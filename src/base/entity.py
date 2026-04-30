from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import MapType


class AbstractEntity(ABC):
    """Абстрактный класс сущности."""

    @abstractmethod
    def to_dict(self) -> MapType:
        pass

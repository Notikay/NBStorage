from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import MapType, MessageType


class AbstractView(ABC):
    """Абстрактный класс формата ответа."""

    @property
    @abstractmethod
    def result(self) -> MapType:
        pass

    @property
    @abstractmethod
    def message(self) -> MessageType:
        pass

    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .types import MessageType


class AbstractError(Exception, ABC):
    """Абстрактный класс ошибки."""

    @property
    @abstractmethod
    def message(self) -> MessageType:
        pass

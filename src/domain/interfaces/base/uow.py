from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from .base_types import (
        UOWErrorType,
        UOWValueErrorType,
        UOWTracebackErrorType
    )


class AbstractUnitOfWork(ABC):
    """Абстрактный класс менеджера состояния транзакции."""

    @abstractmethod
    def __enter__(self) -> Self:
        pass

    @abstractmethod
    def __exit__(
            self,
            exc_type: UOWErrorType,
            exc_val: UOWValueErrorType,
            exc_tb: UOWTracebackErrorType
    ) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

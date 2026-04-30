from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, overload, Sequence

if TYPE_CHECKING:
    from .entity import AbstractEntity
    from .types import MessageType
    from .view import AbstractView


class AbstractPresenter[T: AbstractEntity, U: AbstractView](ABC):
    """Абстрактный класс представления."""

    @overload
    def show_success(self, message: MessageType, result: T) -> U: ...

    @overload
    def show_success(self, message: MessageType) -> U: ...

    @abstractmethod
    def show_success(
            self,
            message: MessageType,
            result: T | Sequence[T] | None = None
    ) -> U:
        pass

    @abstractmethod
    def show_error(self, message: MessageType) -> U:
        pass

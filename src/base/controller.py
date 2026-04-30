from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from .schema import AbstractSchema
    from .view import AbstractView


class AbstractController[T: AbstractSchema, U: AbstractView](ABC):
    """Абстрактный класс контроллера."""

    @overload
    def handle(self, data: T) -> U: ...

    @overload
    def handle(self) -> U: ...

    @abstractmethod
    def handle(self, data: T | None = None) -> U:
        pass

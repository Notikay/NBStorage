from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:
    from .entity import AbstractEntity


class AbstractUseCase[T: AbstractEntity](ABC):
    """Абстрактный класс бизнес-логики."""

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> T | Sequence[T] | None:
        pass

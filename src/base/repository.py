from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:
    from .entity import AbstractEntity


class AbstractRepository[T: AbstractEntity](ABC):
    """Абстрактный класс репозитория."""

    @abstractmethod
    def get_item(self, *args: Any, **kwargs: Any) -> T | None:
        pass

    @abstractmethod
    def get_all_items(self, *args: Any, **kwargs: Any) -> Sequence[T]:
        pass

    @abstractmethod
    def set_item(self, item: T) -> T:
        pass

    @abstractmethod
    def upd_item(self, item: T) -> T | None:
        pass

    @abstractmethod
    def del_item(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def del_all_items(self, *args: Any, **kwargs: Any) -> None:
        pass

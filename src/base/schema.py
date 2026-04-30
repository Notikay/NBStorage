from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AbstractSchema(ABC):
    """Абстрактный класс схемы входных данных."""

    @abstractmethod
    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        pass

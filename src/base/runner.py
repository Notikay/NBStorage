from abc import ABC, abstractmethod
from typing import Any


class AbstractRunner(ABC):
    """Абстрактный класс запуска."""

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        pass

from abc import ABC, abstractmethod
from typing import Any


class AbstractUseCase(ABC):
    """Абстрактный класс бизнес-логики."""

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass

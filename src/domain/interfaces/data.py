from abc import ABC, abstractmethod
from typing import ParamSpec, Any

P = ParamSpec('P')


class AbstractData(ABC):
    """ Абстрактный класс данных."""

    @abstractmethod
    def to_dict(self, *args: P.args, **kwargs: P.kwargs) -> dict[Any, Any]:
        pass


class AbstractCardData(AbstractData):
    """ Абстрактный класс карточки пользователя."""

    @abstractmethod
    def encrypt(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        pass

    @abstractmethod
    def decrypt(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        pass

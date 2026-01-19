from abc import ABC, abstractmethod
from typing import Any, Mapping, TypeVar, Generic

T = TypeVar("T", bound=Mapping[str, Any])


class AbstractData(ABC, Generic[T]):
    """ Абстрактный класс данных."""

    @abstractmethod
    def to_dict(self, *args: Any, **kwargs: Any) -> T:
        pass


class AbstractCard(AbstractData[T]):
    """ Абстрактный класс карточки пользователя."""

    @abstractmethod
    def encrypt(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def decrypt(self, *args: Any, **kwargs: Any) -> Any:
        pass

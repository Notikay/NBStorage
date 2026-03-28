from abc import ABC, abstractmethod
from typing import Any


class AbstractRepository(ABC):
    """Абстрактный класс репозитория хранилища."""

    @abstractmethod
    def get_item(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def get_all(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def set_item(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def upd_item(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def del_item(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def del_all(self, *args: Any, **kwargs: Any) -> Any:
        pass


class AbstractUserRepository(AbstractRepository, ABC):
    """Абстрактный класс репозитория хранилища пользователя."""

    @abstractmethod
    def check_login(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def get_password(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def get_cards_id(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def set_cards_id(self, *args: Any, **kwargs: Any) -> Any:
        pass

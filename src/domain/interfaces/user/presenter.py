from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from base import AbstractPresenter
from .entities import UserEntityInterface
from .view import UserViewInterface

if TYPE_CHECKING:
    from .types import UserMessageType


class UserPresenterInterface(
    AbstractPresenter[UserEntityInterface, UserViewInterface]
):
    """Интерфейс представления пользователя."""

    @abstractmethod
    def show_invalid_error(
            self,
            message: UserMessageType
    ) -> UserViewInterface:
        pass

    @abstractmethod
    def show_not_found(self, message: UserMessageType) -> UserViewInterface:
        pass

    @abstractmethod
    def show_create_error(self, message: UserMessageType) -> UserViewInterface:
        pass

    @abstractmethod
    def show_delete_error(self, message: UserMessageType) -> UserViewInterface:
        pass

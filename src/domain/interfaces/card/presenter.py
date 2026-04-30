from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from base import AbstractPresenter
from .entities import CardEntityInterface
from .view import CardViewInterface

if TYPE_CHECKING:
    from .types import CardMessageType


class CardPresenterInterface(
    AbstractPresenter[CardEntityInterface, CardViewInterface]
):
    """Интерфейс представления карточки пользователя."""

    @abstractmethod
    def show_invalid_error(
            self,
            message: CardMessageType
    ) -> CardViewInterface:
        pass

    @abstractmethod
    def show_not_found(self, message: CardMessageType) -> CardViewInterface:
        pass

    @abstractmethod
    def show_create_error(self, message: CardMessageType) -> CardViewInterface:
        pass

    @abstractmethod
    def show_delete_error(self, message: CardMessageType) -> CardViewInterface:
        pass

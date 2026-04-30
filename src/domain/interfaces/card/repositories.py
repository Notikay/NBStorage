from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, override, Sequence

from base import AbstractRepository

if TYPE_CHECKING:
    from .entities import CardEntityInterface
    from .types import CardMetaUserLoginType, CardMetaCardIDType


class CardRepositoryInterface[T: CardEntityInterface](AbstractRepository[T]):
    """Интерфейс репозитория хранилища карточки пользователя."""

    @override
    @abstractmethod
    def get_item(
            self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType
    ) -> T | None:
        pass

    @override
    @abstractmethod
    def get_all_items(self, user_login: CardMetaUserLoginType) -> Sequence[T]:
        pass

    @override
    @abstractmethod
    def del_item(
            self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType
    ) -> None:
        pass

    @override
    @abstractmethod
    def del_all_items(self, user_login: CardMetaUserLoginType) -> None:
        pass

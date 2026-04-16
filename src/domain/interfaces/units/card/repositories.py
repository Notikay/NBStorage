from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from domain.interfaces import AbstractRepository

if TYPE_CHECKING:
    from domain.interfaces.base.base_types import MapType
    from .entities import CardEntityInterface
    from .card_types import MetaDataUserLoginType, MetaDataCardIDType


class CardRepositoryInterface[T: CardEntityInterface[MapType]](
    AbstractRepository[T],
    ABC
):
    """Интерфейс репозитория хранилища карточки пользователя."""

    @override
    @abstractmethod
    def get_item(
            self,
            user_login: MetaDataUserLoginType,
            card_id: MetaDataCardIDType
    ) -> T | None:
        pass

    @override
    @abstractmethod
    def get_all_items(self, user_login: MetaDataUserLoginType) -> list[T]:
        pass

    @override
    @abstractmethod
    def del_item(
            self,
            user_login: MetaDataUserLoginType,
            card_id: MetaDataCardIDType
    ) -> None:
        pass

    @override
    @abstractmethod
    def del_all_items(self, user_login: MetaDataUserLoginType) -> None:
        pass

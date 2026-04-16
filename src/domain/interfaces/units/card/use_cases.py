from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from domain.interfaces import AbstractUseCase

if TYPE_CHECKING:
    from domain.interfaces.base.base_types import MapType
    from .entities import CardEntityInterface
    from .card_types import (
        MetaDataUserLoginType,
        MetaDataCardIDType,
        MetaDataTitleType,
        MetaDataIconPathType,
        CardParamType,
        CardUpdParamType,
        MetaDataUpdTitleType,
        MetaDataUpdIconPathType
    )


class ChooseCardUseCaseInterface[T: CardEntityInterface[MapType]](
    AbstractUseCase,
    ABC
):
    """Интерфейс бизнес-логики получения карточки пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            user_login: MetaDataUserLoginType,
            card_id: MetaDataCardIDType
    ) -> T:
        pass


class ChooseAllCardsUseCaseInterface[T: CardEntityInterface[MapType]](
    AbstractUseCase,
    ABC
):
    """Интерфейс бизнес-логики получения всех карточек пользователя."""

    @override
    @abstractmethod
    def execute(self, user_login: MetaDataUserLoginType) -> list[T]:
        pass


class CreateCardUseCaseInterface[T: CardEntityInterface[MapType]](
    AbstractUseCase,
    ABC
):
    """Интерфейс бизнес-логики создания карточки пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            user_login: MetaDataUserLoginType,
            title: MetaDataTitleType,
            icon_path: MetaDataIconPathType,
            username: CardParamType,
            email: CardParamType,
            password: CardParamType,
            url: CardParamType,
            description: CardParamType
    ) -> T:
        pass


class DeleteCardUseCaseInterface(AbstractUseCase, ABC):
    """Интерфейс бизнес-логики удаления карточки пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            user_login: MetaDataUserLoginType,
            card_id: MetaDataCardIDType
    ) -> None:
        pass


class DeleteAllCardsUseCaseInterface(AbstractUseCase, ABC):
    """Интерфейс бизнес-логики удаления всех карточек пользователя."""

    @override
    @abstractmethod
    def execute(self, user_login: MetaDataUserLoginType) -> None:
        pass


class UpdateCardUseCaseInterface[T: CardEntityInterface[MapType]](
    AbstractUseCase,
    ABC
):
    """Интерфейс бизнес-логики обновления карточки пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            user_login: MetaDataUserLoginType,
            card_id: MetaDataCardIDType,
            username: CardUpdParamType,
            email: CardUpdParamType,
            password: CardUpdParamType,
            url: CardUpdParamType,
            description: CardUpdParamType
    ) -> T:
        pass


class UpdateMetaDataUseCaseInterface[T: CardEntityInterface[MapType]](
    AbstractUseCase,
    ABC
):
    """
    Интерфейс бизнес-логики обновления метаданных карточки пользователя.
    """

    @override
    @abstractmethod
    def execute(
            self,
            user_login: MetaDataUserLoginType,
            card_id: MetaDataCardIDType,
            title: MetaDataUpdTitleType,
            icon_path: MetaDataUpdIconPathType
    ) -> T:
        pass

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, override, Sequence, Any

from base import AbstractUseCase

if TYPE_CHECKING:
    from .entities import CardEntityInterface
    from .types import (
        CardMetaUserLoginType,
        CardMetaCardIDType,
        CardMetaTitleType,
        CardMetaIconPathType,
        CardParamType,
        CardUpdParamType,
        CardMetaUpdTitleType,
        CardMetaUpdIconPathType
    )


class ChooseCardUseCaseInterface[T: CardEntityInterface](AbstractUseCase[T]):
    """Интерфейс бизнес-логики получения карточки пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType
    ) -> T:
        pass


class ChooseAllCardsUseCaseInterface[T: CardEntityInterface](
    AbstractUseCase[T]
):
    """Интерфейс бизнес-логики получения всех карточек пользователя."""

    @override
    @abstractmethod
    def execute(self, user_login: CardMetaUserLoginType) -> Sequence[T]:
        pass


class CreateCardUseCaseInterface[T: CardEntityInterface](AbstractUseCase[T]):
    """Интерфейс бизнес-логики создания карточки пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            user_login: CardMetaUserLoginType,
            title: CardMetaTitleType,
            icon_path: CardMetaIconPathType,
            username: CardParamType,
            email: CardParamType,
            password: CardParamType,
            url: CardParamType,
            description: CardParamType
    ) -> T:
        pass


class DeleteCardUseCaseInterface(AbstractUseCase[Any]):
    """Интерфейс бизнес-логики удаления карточки пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType
    ) -> None:
        pass


class DeleteAllCardsUseCaseInterface(AbstractUseCase[Any]):
    """Интерфейс бизнес-логики удаления всех карточек пользователя."""

    @override
    @abstractmethod
    def execute(self, user_login: CardMetaUserLoginType) -> None:
        pass


class UpdateCardUseCaseInterface[T: CardEntityInterface](AbstractUseCase[T]):
    """Интерфейс бизнес-логики обновления карточки пользователя."""

    @override
    @abstractmethod
    def execute(
            self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType,
            username: CardUpdParamType,
            email: CardUpdParamType,
            password: CardUpdParamType,
            url: CardUpdParamType,
            description: CardUpdParamType
    ) -> T:
        pass


class UpdateCardMetaUseCaseInterface[T: CardEntityInterface](
    AbstractUseCase[T]
):
    """
    Интерфейс бизнес-логики обновления метаданных карточки пользователя.
    """

    @override
    @abstractmethod
    def execute(
            self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType,
            title: CardMetaUpdTitleType,
            icon_path: CardMetaUpdIconPathType
    ) -> T:
        pass

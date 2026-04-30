from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import Card
from domain.interfaces import UpdateCardMetaUseCaseInterface
from .exceptions import CardNotFoundError

if TYPE_CHECKING:
    from domain.interfaces import CardUnitOfWorkInterface
    from domain.interfaces.card.types import (
        CardMetaUserLoginType,
        CardMetaCardIDType,
        CardMetaUpdTitleType,
        CardMetaUpdIconPathType
    )


class UpdateCardMeta(UpdateCardMetaUseCaseInterface[Card]):
    """Обновление метаданных карточки пользователя."""

    def __init__(self, uow: CardUnitOfWorkInterface[Card]):
        """
        Инициализация получения карточки пользователя.

        :param uow: Менеджер управления транзакцией карточки
                    пользователя.
        :type uow: CardUnitOfWorkInterface
        """
        self.__uow = uow

    def execute(
            self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType,
            title: CardMetaUpdTitleType,
            icon_path: CardMetaUpdIconPathType
    ) -> Card:
        """
        Обновление метаданных карточки пользователя.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: CardMetaCardIDType

        :param title: Название карточки пользователя.
        :type title: CardMetaUpdTitleType

        :param icon_path: Путь к иконке карточки пользователя.
        :type icon_path: CardMetaUpdIconPathType

        :return: Карточка пользователя.
        :rtype: Card

        :raises CardNotFoundError: Если карточка пользователя не
                                   найдена.
        """
        with self.__uow:
            card = self.__uow.card_repos.get_item(user_login, card_id)
            if card is None:
                raise CardNotFoundError(user_login, card_id)

            # Mypy ругается на разные типы для property и setter
            card.meta.title = title  # type: ignore
            card.meta.icon_path = icon_path  # type: ignore

            upd_card: Card | None = self.__uow.card_repos.upd_item(card)
            if upd_card is None:
                raise CardNotFoundError(user_login, card_id)
            upd_card.decrypt()

            self.__uow.commit()

            return upd_card

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.card import UpdateMetaDataUseCaseInterface
from domain.entities import Card
from .exceptions import CardNotFoundError

if TYPE_CHECKING:
    from domain.interfaces.units.card import CardUnitOfWorkInterface
    from domain.interfaces.units.card.card_types import (
        MetaDataUserLoginType,
        MetaDataCardIDType,
        MetaDataUpdTitleType,
        MetaDataUpdIconPathType
    )


class UpdateMetaData(UpdateMetaDataUseCaseInterface[Card]):
    """
    Обновление метаданных карточки пользователя.

    :ivar __uow: Атрибут менеджера состояния транзакции карточки
                 пользователя.
    :type __uow: CardUnitOfWorkInterface
    """

    def __init__(self, uow: CardUnitOfWorkInterface[Card]):
        """
        Инициализация получения карточки пользователя.

        :param uow: Менеджер состояния транзакции карточки пользователя.
        :type uow: CardUnitOfWorkInterface
        """
        self.__uow = uow

    def execute(
            self,
            user_login: MetaDataUserLoginType,
            card_id: MetaDataCardIDType,
            title: MetaDataUpdTitleType,
            icon_path: MetaDataUpdIconPathType
    ) -> Card:
        """
        Обновление метаданных карточки пользователя.

        :param user_login: Логин пользователя.
        :type user_login: MetaDataUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: MetaDataCardIDType

        :param title: Название карточки пользователя.
        :type title: MetaDataUpdTitleType

        :param icon_path: Путь к иконке карточки пользователя.
        :type icon_path: MetaDataUpdIconPathType

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
            card.metadata.title = title  # type: ignore
            card.metadata.icon_path = icon_path  # type: ignore

            card = self.__uow.card_repos.upd_item(card)
            if card is None:
                raise CardNotFoundError(user_login, card_id)
            card.decrypt()

            self.__uow.commit()

            return card

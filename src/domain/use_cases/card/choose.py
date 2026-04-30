from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import Card
from domain.interfaces import ChooseCardUseCaseInterface
from .exceptions import CardNotFoundError

if TYPE_CHECKING:
    from domain.interfaces import CardUnitOfWorkInterface
    from domain.interfaces.card.types import (
        CardMetaUserLoginType,
        CardMetaCardIDType
    )


class ChooseCard(ChooseCardUseCaseInterface[Card]):
    """Получение карточки пользователя."""

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
            card_id: CardMetaCardIDType
    ) -> Card:
        """
        Получение карточки пользователя.

        Получение карточки пользователя из хранилища.
        Расшифровка карточки пользователя.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: CardMetaCardIDType

        :return: Карточка пользователя.
        :rtype: Card

        :raises CardNotFoundError: Если карточка пользователя не
                                   найдена.
        """
        with self.__uow:
            card = self.__uow.card_repos.get_item(user_login, card_id)
            if card is None:
                raise CardNotFoundError(user_login, card_id)
            card.decrypt()

            self.__uow.commit()

            return card

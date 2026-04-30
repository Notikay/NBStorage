from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import Card
from domain.interfaces import ChooseAllCardsUseCaseInterface

if TYPE_CHECKING:
    from domain.interfaces import CardUnitOfWorkInterface
    from domain.interfaces.card.types import CardMetaUserLoginType


class ChooseAllCards(ChooseAllCardsUseCaseInterface[Card]):
    """Получение всех карточек пользователя."""

    def __init__(self, uow: CardUnitOfWorkInterface[Card]):
        """
        Инициализация получения карточки пользователя.

        :param uow: Менеджер управления транзакцией карточки
                    пользователя.
        :type uow: CardUnitOfWorkInterface
        """
        self.__uow = uow

    def execute(self, user_login: CardMetaUserLoginType) -> list[Card]:
        """
        Получение всех карточек пользователя.

        Получение всех карточек пользователя из хранилища.
        Расшифровка всех карточек пользователя.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :return: Все карточки пользователя.
        :rtype: list[Card]
        """
        with self.__uow:
            cards = list(self.__uow.card_repos.get_all_items(user_login))
            for i, card in enumerate(cards):
                card.decrypt()

            self.__uow.commit()

            return cards

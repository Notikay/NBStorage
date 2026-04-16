from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.card import ChooseAllCardsUseCaseInterface
from domain.entities import Card

if TYPE_CHECKING:
    from domain.interfaces.units.card import CardUnitOfWorkInterface
    from domain.interfaces.units.card.card_types import MetaDataUserLoginType


class ChooseAllCards(ChooseAllCardsUseCaseInterface[Card]):
    """
    Получение всех карточек пользователя.

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

    def execute(self, user_login: MetaDataUserLoginType) -> list[Card]:
        """
        Получение всех карточек пользователя.

        Получение всех карточек пользователя из хранилища.
        Расшифровка всех карточек пользователя.

        :param user_login: Логин пользователя.
        :type user_login: MetaDataUserLoginType

        :return: Все карточки пользователя.
        :rtype: list[Card]
        """
        with self.__uow:
            cards = self.__uow.card_repos.get_all_items(user_login)
            for i, card in enumerate(cards):
                card.decrypt()

            self.__uow.commit()

            return cards

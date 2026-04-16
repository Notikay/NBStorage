from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.card import DeleteAllCardsUseCaseInterface
from domain.entities import Card

if TYPE_CHECKING:
    from domain.interfaces.units.card import CardUnitOfWorkInterface
    from domain.interfaces.units.card.card_types import MetaDataUserLoginType


class DeleteAllCards(DeleteAllCardsUseCaseInterface):
    """
    Удаление всех карточек пользователя.

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

    def execute(self, user_login: MetaDataUserLoginType) -> None:
        """
        Удаление всех карточек пользователя.

        :param user_login: Логин пользователя.
        :type user_login: MetaDataUserLoginType
        """
        with self.__uow:
            self.__uow.card_repos.del_all_items(user_login)
            self.__uow.commit()

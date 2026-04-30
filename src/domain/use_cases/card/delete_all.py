from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import Card
from domain.interfaces import DeleteAllCardsUseCaseInterface

if TYPE_CHECKING:
    from domain.interfaces import CardUnitOfWorkInterface
    from domain.interfaces.card.types import CardMetaUserLoginType


class DeleteAllCards(DeleteAllCardsUseCaseInterface):
    """Удаление всех карточек пользователя."""

    def __init__(self, uow: CardUnitOfWorkInterface[Card]):
        """
        Инициализация получения карточки пользователя.

        :param uow: Менеджер управления транзакцией карточки
                    пользователя.
        :type uow: CardUnitOfWorkInterface
        """
        self.__uow = uow

    def execute(self, user_login: CardMetaUserLoginType) -> None:
        """
        Удаление всех карточек пользователя.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType
        """
        with self.__uow:
            self.__uow.card_repos.del_all_items(user_login)
            self.__uow.commit()

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import Card
from domain.interfaces import DeleteCardUseCaseInterface

if TYPE_CHECKING:
    from domain.interfaces import CardUnitOfWorkInterface
    from domain.interfaces.card.types import (
        CardMetaUserLoginType,
        CardMetaCardIDType
    )


class DeleteCard(DeleteCardUseCaseInterface):
    """Удаление карточки пользователя."""

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
    ) -> None:
        """
        Удаление карточки пользователя.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: CardMetaCardIDType
        """
        with self.__uow:
            self.__uow.card_repos.del_item(user_login, card_id)
            self.__uow.commit()

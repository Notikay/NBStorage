from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.card import DeleteCardUseCaseInterface
from domain.entities import Card

if TYPE_CHECKING:
    from domain.interfaces.units.card import CardUnitOfWorkInterface
    from domain.interfaces.units.card.card_types import (
        MetaDataUserLoginType,
        MetaDataCardIDType
    )


class DeleteCard(DeleteCardUseCaseInterface):
    """
    Удаление карточки пользователя.

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
            card_id: MetaDataCardIDType
    ) -> None:
        """
        Удаление карточки пользователя.

        :param user_login: Логин пользователя.
        :type user_login: MetaDataUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: MetaDataCardIDType
        """
        with self.__uow:
            self.__uow.card_repos.del_item(user_login, card_id)
            self.__uow.commit()

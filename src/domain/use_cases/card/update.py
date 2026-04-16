from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.card import UpdateCardUseCaseInterface
from domain.entities import Card
from .exceptions import CardNotFoundError

if TYPE_CHECKING:
    from domain.interfaces.units.card import CardUnitOfWorkInterface
    from domain.interfaces.units.card.card_types import (
        MetaDataUserLoginType,
        MetaDataCardIDType,
        CardUpdParamType,
    )


class UpdateCard(UpdateCardUseCaseInterface[Card]):
    """
    Обновление карточки пользователя.

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
            username: CardUpdParamType,
            email: CardUpdParamType,
            password: CardUpdParamType,
            url: CardUpdParamType,
            description: CardUpdParamType
    ) -> Card:
        """
        Обновление карточки пользователя.

        Получение карточки пользователя из хранилища.
        Расшифровка карточки пользователя.
        Обновление карточки пользователя.
        Шифровка карточки пользователя.
        Сохранение карточки пользователя в хранилище.

        :param user_login: Логин пользователя.
        :type user_login: MetaDataUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: MetaDataCardIDType

        :param username: Имя пользователя от сервиса.
        :type username: CardUpdParamType

        :param email: Электронная почта привязанная к сервису.
        :type email: CardUpdParamType

        :param password: Пароль от сервиса.
        :type password: CardUpdParamType

        :param url: URL-адрес сервиса.
        :type url: CardUpdParamType

        :param description: Описание сервиса.
        :type description: CardUpdParamType

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

            card.username = username
            card.email = email
            card.password = password
            card.url = url
            card.description = description
            card.encrypt()

            card = self.__uow.card_repos.upd_item(card)
            if card is None:
                raise CardNotFoundError(user_login, card_id)
            card.decrypt()

            self.__uow.commit()

            return card

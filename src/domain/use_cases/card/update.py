from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import Card
from domain.interfaces import UpdateCardUseCaseInterface
from .exceptions import CardNotFoundError

if TYPE_CHECKING:
    from domain.interfaces import CardUnitOfWorkInterface
    from domain.interfaces.card.types import (
        CardMetaUserLoginType,
        CardMetaCardIDType,
        CardUpdParamType,
    )


class UpdateCard(UpdateCardUseCaseInterface[Card]):
    """Обновление карточки пользователя."""

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
        :type user_login: CardMetaUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: CardMetaCardIDType

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

            upd_card: Card | None = self.__uow.card_repos.upd_item(card)
            if upd_card is None:
                raise CardNotFoundError(user_login, card_id)
            upd_card.decrypt()

            self.__uow.commit()

            return upd_card

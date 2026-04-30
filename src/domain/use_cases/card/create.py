from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import Card, CardMeta
from domain.interfaces import CreateCardUseCaseInterface

if TYPE_CHECKING:
    from domain.interfaces import CardUnitOfWorkInterface
    from domain.interfaces.card.types import (
        CardMetaUserLoginType,
        CardMetaTitleType,
        CardMetaIconPathType,
        CardParamType
    )


class CreateCard(CreateCardUseCaseInterface[Card]):
    """Создание карточки пользователя."""

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
            title: CardMetaTitleType,
            icon_path: CardMetaIconPathType,
            username: CardParamType,
            email: CardParamType,
            password: CardParamType,
            url: CardParamType,
            description: CardParamType
    ) -> Card:
        """
        Создание карточки пользователя.

        Формирование карточки пользователя.
        Шифрование карточки пользователя.
        Сохранение карточки пользователя в хранилище.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :param title: Название карточки пользователя.
        :type title: CardMetaTitleType

        :param icon_path: Путь к иконке карточки пользователя.
        :type icon_path: CardMetaIconPathType

        :param username: Имя пользователя от сервиса.
        :type username: CardParamType

        :param email: Электронная почта привязанная к сервису.
        :type email: CardParamType

        :param password: Пароль от сервиса.
        :type password: CardParamType

        :param url: URL-адрес сервиса.
        :type url: CardParamType

        :param description: Описание сервиса.
        :type description: CardParamType

        :return: Карточка пользователя.
        :rtype: Card
        """
        with self.__uow:
            card = Card(
                CardMeta(title, icon_path, user_login),
                username,
                email,
                password,
                url,
                description
            )
            card.encrypt()

            card = self.__uow.card_repos.set_item(card)
            card.decrypt()

            self.__uow.commit()

            return card

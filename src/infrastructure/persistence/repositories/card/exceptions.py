from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces import (
    CreateCardErrorInterface,
    DeleteCardErrorInterface
)

if TYPE_CHECKING:
    from domain.interfaces.card.types import (
        CardMetaUserLoginType,
        CardMetaCardIDType,
        CardMessageType
    )


class CardCreateError(CreateCardErrorInterface):
    """Ошибка при создании карточки пользователя в хранилище."""

    def __init__(
            self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType
    ):
        """
        Инициализация ошибки.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: CardMetaCardIDType
        """
        self.__user_login = user_login
        self.__card_id = card_id

    @override
    @property
    def message(self) -> CardMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: CardMessageType
        """
        return ("Ошибка создания карточки пользователя в хранилище! -> "
                f"{self.__card_id} ({self.__user_login})")


class CardDeleteError(DeleteCardErrorInterface):
    """Ошибка удаления карточки пользователя из хранилища."""

    def __init__(
            self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType
    ):
        """
        Инициализация ошибки.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: CardMetaCardIDType
        """
        self.__user_login = user_login
        self.__card_id = card_id

    @override
    @property
    def message(self) -> CardMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: CardMessageType
        """
        return ("Ошибка удаления карточки пользователя из хранилища! -> "
                f"{self.__card_id} ({self.__user_login})")


class CardDeleteAllError(DeleteCardErrorInterface):
    """Ошибка удаления всех карточек пользователя из хранилища."""

    def __init__(self, user_login: CardMetaUserLoginType):
        """
        Инициализация ошибки.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType
        """
        self.__user_login = user_login

    @override
    @property
    def message(self) -> CardMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: CardMessageType
        """
        return ("Ошибка удаления всех карточек пользователя из хранилища! -> "
                f"{self.__user_login}")

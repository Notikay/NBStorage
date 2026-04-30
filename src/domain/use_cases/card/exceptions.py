from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces import CardNotFoundErrorInterface

if TYPE_CHECKING:
    from domain.interfaces.card.types import (
        CardMetaUserLoginType,
        CardMetaCardIDType,
        CardMessageType
    )


class CardNotFoundError(CardNotFoundErrorInterface):
    """Ошибка при не найденной карточке пользователя."""

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
        return ("Карточка пользователя не найдена! -> "
                f"{self.__card_id} ({self.__user_login})")

from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces import CardSessionNotInitializedErrorInterface
from domain.interfaces import UserSessionNotInitializedErrorInterface

if TYPE_CHECKING:
    from domain.interfaces.card.types import CardMessageType
    from domain.interfaces.user.types import UserMessageType


class SessionNotInitializedError(
    CardSessionNotInitializedErrorInterface,
    UserSessionNotInitializedErrorInterface
):
    """Ошибка инициализации сессии подключения к хранилищу."""

    def __init__(self, msg: str | None = None):
        """
        Инициализация ошибки.

        :param msg: Подробное описание ошибки.
        :type msg: str | None
        """
        self.__msg = msg

    @override
    @property
    def message(self) -> CardMessageType | UserMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: str
        """
        if self.__msg:
            return self.__msg
        return "Ошибка инициализации сессии подключения к хранилищу!"

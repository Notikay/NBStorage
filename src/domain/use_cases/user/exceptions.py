from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces import UserNotFoundErrorInterface

if TYPE_CHECKING:
    from domain.interfaces.user.types import UserLoginType, UserMessageType


class UserNotFoundError(UserNotFoundErrorInterface):
    """Ошибка при не найденном пользователе."""

    def __init__(self, login: UserLoginType):
        """
        Инициализация ошибки.

        :param login: Логин пользователя.
        :type login: UserLoginType
        """
        self.__login = login

    @override
    @property
    def message(self) -> UserMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: UserMessageType
        """
        return f"Пользователь не найден! -> {self.__login}"

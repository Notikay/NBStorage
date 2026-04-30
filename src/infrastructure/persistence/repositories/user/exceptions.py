from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces import (
    CreateUserErrorInterface,
    DeleteUserErrorInterface
)

if TYPE_CHECKING:
    from domain.interfaces.user.types import UserLoginType, UserMessageType


class UserCreateError(CreateUserErrorInterface):
    """Ошибка создания пользователя в хранилище."""

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
        return f"Ошибка создания пользователя в хранилище! -> {self.__login}"


class UserDeleteError(DeleteUserErrorInterface):
    """Ошибка удаления пользователя из хранилища."""

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
        return f"Ошибка удаления пользователя из хранилища! -> {self.__login}"


class UserDeleteAllError(DeleteUserErrorInterface):
    """Ошибка удаления всех пользователей из хранилища."""

    @override
    @property
    def message(self) -> UserMessageType:
        """
         Сообщение об ошибке.

         :return: Текст ошибки.
         :rtype: UserMessageType
         """
        return "Ошибка удаления всех пользователей из хранилища!"

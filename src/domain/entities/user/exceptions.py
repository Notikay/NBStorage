from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces import UserInvalidErrorInterface

if TYPE_CHECKING:
    from domain.interfaces.user.types import (
        UserMetaNameType,
        UserMessageType,
        UserMetaAvatarPathType,
        UserMetaTimeBlockType,
        UserLoginType,
        UserPasswordType
    )


class UserMetaInvalidNameError(UserInvalidErrorInterface):
    """Ошибка метаданных пользователя, при некорректном имени."""

    def __init__(self, name: UserMetaNameType):
        """
        Инициализация ошибки.

        :param name: Название карточки пользователя.
        :type name: UserMetaNameType
        """
        self.__name = name

    @override
    @property
    def message(self) -> UserMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: UserMessageType
        """
        return f"Некорректное имя пользователя! -> {self.__name}"


class UserMetaInvalidAvatarPathError(UserInvalidErrorInterface):
    """
    Ошибка метаданных пользователя, при некорректном пути к аватарке.
    """

    def __init__(self, avatar_path: UserMetaAvatarPathType):
        """
        Инициализация ошибки.

        :param avatar_path: Путь к аватарке пользователя.
        :type avatar_path: UserMetaAvatarPathType
        """
        self.__avatar_path = avatar_path

    @override
    @property
    def message(self) -> UserMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: UserMessageType
        """
        return ("Некорректный путь к аватарке пользователя! -> "
                f"{self.__avatar_path}")


class UserMetaInvalidTimeBlockError(UserInvalidErrorInterface):
    """
    Ошибка метаданных пользователя, при некорректном времени блокировки
    сессии.
    """

    def __init__(self, time_block: UserMetaTimeBlockType):
        """
        Инициализация ошибки.

        :param time_block: Время блокировки сессии пользователя.
        :type time_block: UserMetaTimeBlockType
        """
        self.__time_block = time_block

    @override
    @property
    def message(self) -> UserMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: UserMessageType
        """
        return ("Некорректное время блокировки сессии пользователя! -> "
                f"{self.__time_block}")


class UserInvalidLoginError(UserInvalidErrorInterface):
    """Ошибка пользователя, при некорректном логине."""

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
        return f"Некорректный логин пользователя! -> {self.__login}"


class UserInvalidPasswordError(UserInvalidErrorInterface):
    """Ошибка пользователя, при некорректном пароле."""

    def __init__(self, password: UserPasswordType):
        """
        Инициализация ошибки.

        :param password: Пароль пользователя.
        :type password: UserPasswordType
        """
        self.__password = password

    @override
    @property
    def message(self) -> UserMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: UserMessageType
        """
        return f"Некорректный пароль пользователя! -> {self.__password!r}"

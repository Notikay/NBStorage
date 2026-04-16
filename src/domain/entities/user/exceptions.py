from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces.units.user.exceptions import UserEntityError

if TYPE_CHECKING:
    from domain.interfaces.units.user.user_types import (
        SettingsNameType,
        SettingsAvatarPathType,
        SettingsTimeBlockType,
        UserLoginType,
        UserPasswordType
    )


class SettingsInvalidNameError(UserEntityError):
    """
    Ошибка настроек пользователя, при некорректном имени.

    :ivar name: Атрибут имени пользователя.
    :type name: SettingsNameType

    :ivar msg: Атрибут подробного описания ошибки.
    :type msg: str | None
    """

    def __init__(self, name: SettingsNameType, msg: str | None = None):
        """
        Инициализация ошибки.

        :param name: Имя пользователя.
        :type name: SettingsNameType

        :param msg: Подробное описание ошибки.
        :type msg: str | None
        """
        self.name = name
        self.msg = msg

    @override
    @property
    def message(self) -> str:
        if self.msg:
            return f"{self.msg} -> {self.name}"
        return f"Некорректное имя пользователя! -> {self.name}"


class SettingsInvalidAvatarPathError(UserEntityError):
    """
    Ошибка настроек пользователя, при некорректном пути к аватарке.

    :ivar avatar_path: Атрибут пути к аватарке пользователя.
    :type avatar_path: SettingsAvatarPathType

    :ivar msg: Атрибут подробного описания ошибки.
    :type msg: str | None
    """

    def __init__(
            self,
            avatar_path: SettingsAvatarPathType,
            msg: str | None = None
    ):
        """
        Инициализация ошибки.

        :param avatar_path: Путь к аватарке пользователя.
        :type avatar_path: SettingsAvatarPathType

        :param msg: Подробное описание ошибки.
        :type msg: str | None
        """
        self.avatar_path = avatar_path
        self.msg = msg

    @override
    @property
    def message(self) -> str:
        if self.msg:
            return f"{self.msg} -> {self.avatar_path}"
        return ("Некорректный путь к аватарке пользователя! -> "
                f"{self.avatar_path}")


class SettingsInvalidTimeBlockError(UserEntityError):
    """
    Ошибка настроек пользователя, при некорректном времени блокировки
    сессии.

    :ivar time_block: Атрибут времени блокировки сессии пользователя.
    :type time_block: SettingsTimeBlockType

    :ivar msg: Атрибут подробного описания ошибки.
    :type msg: str | None
    """

    def __init__(
            self,
            time_block: SettingsTimeBlockType,
            msg: str | None = None
    ):
        """
        Инициализация ошибки.

        :param time_block: Время блокировки сессии пользователя.
        :type time_block: SettingsTimeBlockType

        :param msg: Подробное описание ошибки.
        :type msg: str | None
        """
        self.time_block = time_block
        self.msg = msg

    @override
    @property
    def message(self) -> str:
        if self.msg:
            return f"{self.msg} -> {self.time_block}"
        return ("Некорректное время блокировки сессии пользователя! -> "
                f"{self.time_block}")


class UserInvalidLoginError(UserEntityError):
    """
    Ошибка пользователя, при некорректном логине.

    :ivar login: Атрибут логина пользователя.
    :type login: UserLoginType

    :ivar msg: Атрибут подробного описания ошибки.
    :type msg: str | None
    """

    def __init__(self, login: UserLoginType, msg: str | None = None):
        """
        Инициализация ошибки.

        :param login: Логин пользователя.
        :type login: UserLoginType

        :param msg: Подробное описание ошибки.
        :type msg: str | None
        """
        self.login = login
        self.msg = msg

    @override
    @property
    def message(self) -> str:
        if self.msg:
            return f"{self.msg} -> {self.login}"
        return f"Некорректный логин пользователя! -> {self.login}"


class UserInvalidPasswordError(UserEntityError):
    """
    Ошибка пользователя, при некорректном пароле.

    :ivar password: Атрибут пароля пользователя.
    :type password: UserPasswordType

    :ivar msg: Атрибут подробного описания ошибки.
    :type msg: str | None
    """

    def __init__(self, password: UserPasswordType, msg: str | None = None):
        """
        Инициализация ошибки.

        :param password: Пароль пользователя.
        :type password: UserPasswordType

        :param msg: Подробное описание ошибки.
        :type msg: str | None
        """
        self.password = password
        self.msg = msg

    @override
    @property
    def message(self) -> str:
        if self.msg:
            return f"{self.msg} -> {self.password!r}"
        return f"Некорректный пароль пользователя! -> {self.password!r}"

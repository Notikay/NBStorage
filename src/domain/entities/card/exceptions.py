from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces import CardInvalidErrorInterface

if TYPE_CHECKING:
    from domain.interfaces.card.types import (
        CardMetaTitleType,
        CardMessageType,
        CardMetaIconPathType,
        CardMetaUserLoginType,
        CardParamType
    )


class CardMetaInvalidTitleError(CardInvalidErrorInterface):
    """
    Ошибка метаданных карточки пользователя, при некорректном названии.
    """

    def __init__(self, title: CardMetaTitleType):
        """
        Инициализация ошибки.

        :param title: Название карточки пользователя.
        :type title: CardMetaTitleType
        """
        self.__title = title

    @override
    @property
    def message(self) -> CardMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: CardMessageType
        """
        return ("Некорректное название карточки пользователя! -> "
                f"{self.__title}")


class CardMetaInvalidIconPathError(CardInvalidErrorInterface):
    """
    Ошибка метаданных карточки пользователя, при некорректном пути к
    иконке.
    """

    def __init__(self, icon_path: CardMetaIconPathType):
        """
        Инициализация ошибки.

        :param icon_path: Путь к иконке карточки пользователя.
        :type icon_path: CardMetaIconPathType
        """
        self.__icon_path = icon_path

    @override
    @property
    def message(self) -> CardMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: CardMessageType
        """
        return ("Некорректный путь к иконке карточки пользователя! -> "
                f"{self.__icon_path}")


class CardMetaInvalidUserLoginError(CardInvalidErrorInterface):
    """
    Ошибка метаданных карточки пользователя, при некорректном логине.
    """

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
        return f"Некорректный логин пользователя! -> {self.__user_login}"


class CardInvalidParamError(CardInvalidErrorInterface):
    """
    Ошибка карточки пользователя, при некорректном значении параметра.
    """

    def __init__(
            self,
            param: CardParamType,
            param_name: str,
            msg: str | None = None
    ):
        """
        Инициализация ошибки.

        :param param: Значение параметра в карточке пользователя.
        :type param: CardParamType

        :param param_name: Название параметра в карточке пользователя.
        :type param_name: str

        :param msg: Подробное описание ошибки.
        :type msg: str | None
        """
        self.__param = param
        self.__param_name = param_name
        self.__msg = msg

    @override
    @property
    def message(self) -> CardMessageType:
        """
        Сообщение об ошибке.

        :return: Текст ошибки.
        :rtype: CardMessageType
        """
        if self.__msg:
            return f"{self.__msg} -> {self.__param_name}: {self.__param!r}"
        return ("Некорректное значение параметра в карточке пользователя! -> "
                f"{self.__param_name}: {self.__param!r}")

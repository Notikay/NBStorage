from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces.units.card.exceptions import CardEntityError

if TYPE_CHECKING:
    from domain.interfaces.units.card.card_types import (
        MetaDataTitleType,
        MetaDataIconPathType,
        MetaDataUserLoginType,
        CardParamType
    )


class MetaDataInvalidTitleError(CardEntityError):
    """
    Ошибка метаданных карточки пользователя, при некорректном названии.

    :ivar title: Атрибут названия карточки пользователя.
    :type title: MetaDataTitleType

    :ivar msg: Атрибут подробного описания ошибки.
    :type msg: str | None
    """

    def __init__(self, title: MetaDataTitleType, msg: str | None = None):
        """
        Инициализация ошибки.

        :param title: Название карточки пользователя.
        :type title: MetaDataTitleType

        :param msg: Подробное описание ошибки.
        :type msg: str | None
        """
        self.title = title
        self.msg = msg

    @override
    @property
    def message(self) -> str:
        if self.msg:
            return f"{self.msg} -> {self.title}"
        return f"Некорректное название карточки пользователя! -> {self.title}"


class MetaDataInvalidIconPathError(CardEntityError):
    """
    Ошибка метаданных карточки пользователя, при некорректном пути к
    иконке.

    :ivar icon_path: Атрибут пути к иконке карточки пользователя.
    :type icon_path: MetaDataIconPathType

    :ivar msg: Атрибут подробного описания ошибки.
    :type msg: str | None
    """

    def __init__(
            self,
            icon_path: MetaDataIconPathType,
            msg: str | None = None
    ):
        """
        Инициализация ошибки.

        :param icon_path: Путь к иконке карточки пользователя.
        :type icon_path: MetaDataIconPathType

        :param msg: Подробное описание ошибки.
        :type msg: str | None
        """
        self.icon_path = icon_path
        self.msg = msg

    @override
    @property
    def message(self) -> str:
        if self.msg:
            return f"{self.msg} -> {self.icon_path}"
        return ("Некорректный путь к иконке карточки пользователя! -> "
                f"{self.icon_path}")


class MetaDataInvalidUserLoginError(CardEntityError):
    """
    Ошибка метаданных карточки пользователя, при некорректном логине.

    :ivar user_login: Атрибут логина пользователя.
    :type user_login: MetaDataUserLoginType

    :ivar msg: Атрибут подробного описания ошибки.
    :type msg: str | None
    """

    def __init__(
            self,
            user_login: MetaDataUserLoginType,
            msg: str | None = None
    ):
        """
        Инициализация ошибки.

        :param user_login: Логин пользователя.
        :type user_login: MetaDataUserLoginType

        :param msg: Подробное описание ошибки.
        :type msg: str | None
        """
        self.user_login = user_login
        self.msg = msg

    @override
    @property
    def message(self) -> str:
        if self.msg:
            return f"{self.msg} -> {self.user_login}"
        return f"Некорректный логин пользователя! -> {self.user_login}"


class CardInvalidParamFieldError(CardEntityError):
    """
    Ошибка карточки пользователя, при некорректном значении параметра.

    :ivar param: Атрибут значения параметра в карточке пользователя.
    :type param: CardParamType

    :ivar param_name: Атрибут названия параметра в карточке
                      пользователя.
    :type param_name: str

    :ivar msg: Атрибут подробного описания ошибки.
    :type msg: str | None
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
        self.param = param
        self.param_name = param_name
        self.msg = msg

    @override
    @property
    def message(self) -> str:
        if self.msg:
            return f"{self.msg} -> {self.param_name}: {self.param!r}"
        return ("Некорректное значение параметра в карточке пользователя! -> "
                f"{self.param_name}: {self.param!r}")

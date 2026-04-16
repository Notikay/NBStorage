from __future__ import annotations

import secrets
import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from domain.interfaces import AbstractEntity
from .dto import MetaDataDTO
from .exceptions import (
    MetaDataInvalidIconPathError,
    MetaDataInvalidTitleError,
    MetaDataInvalidUserLoginError
)

if TYPE_CHECKING:
    from domain.interfaces.units.card.card_types import (
        MetaDataTitleType,
        MetaDataIconPathType,
        MetaDataUserLoginType,
        MetaDataCardIDType,
        MetaDataUpdTitleType,
        MetaDataUpdIconPathType
    )


@dataclass(slots=True)
class MetaData(AbstractEntity[MetaDataDTO]):
    """
    Метаданные карточки пользователя.

    :var _title: Атрибут названия карточки пользователя.
    :type _title: MetaDataTitleType

    :var _icon_path: Атрибут пути к иконке карточки пользователя.
    :type _icon_path: MetaDataIconPathType

    :var _user_login: Атрибут логина пользователя, которому принадлежит
                      карточка.
    :type _user_login: MetaDataUserLoginType

    :var __key: Атрибут ключа шифрования для данных карточки
                пользователя.
    :type __key: bytes

    :var __card_id: Атрибут ID карточки пользователя.
    :type __card_id: MetaDataCardIDType

    :cvar __ICON_EXTS: Атрибут поддерживаемых расширений иконок карточки
                       пользователя.
    :type __ICON_EXTS: set[str]
    """
    _title: MetaDataTitleType
    _icon_path: MetaDataIconPathType
    _user_login: MetaDataUserLoginType

    __key: bytes = field(
        default_factory=lambda: secrets.token_bytes(32),
        init=True,
        repr=False
    )
    __card_id: MetaDataCardIDType = field(init=False)

    __ICON_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.ico', '.icon'}

    @property
    def user_login(self) -> MetaDataUserLoginType:
        return self._user_login

    @property
    def key(self) -> bytes:
        return self.__key

    @property
    def card_id(self) -> uuid.UUID:
        return self.__card_id

    @property
    def title(self) -> MetaDataTitleType:
        return self._title

    @title.setter
    def title(self, value: MetaDataUpdTitleType) -> None:
        self._update_field('_title', value, self.__check_empty_title)

    @property
    def icon_path(self) -> MetaDataIconPathType:
        return self._icon_path

    @icon_path.setter
    def icon_path(self, value: MetaDataUpdIconPathType) -> None:
        self._update_field(
            '_icon_path',
            value,
            self.__check_incorrect_icon_path
        )

    def to_dict(self) -> MetaDataDTO:
        """
        Преобразование в словарь.

        Путь к иконке карточки пользователя и ID карточки пользователя
        преобразуются в строки.

        :return: Словарь с метаданными карточки пользователя.
        :rtype: MetaDataDTO
        """
        return {
            'title': self._title,
            'icon_path': str(self._icon_path),
            'user_login': self._user_login,
            'card_id': str(self.__card_id)
        }

    def __generate_card_id(self) -> MetaDataCardIDType:
        return uuid.uuid5(
            uuid.NAMESPACE_OID,
            name=f"{self._user_login}-{self.__key.hex()}"
        )

    @classmethod
    def __check_incorrect_icon_path(
            cls,
            icon_path: MetaDataIconPathType
    ) -> None:
        if icon_path.suffix.lower() not in cls.__ICON_EXTS:
            raise MetaDataInvalidIconPathError(icon_path)

    @staticmethod
    def __check_empty_title(title: MetaDataTitleType) -> None:
        if not title:
            raise MetaDataInvalidTitleError(title)

    @staticmethod
    def __check_empty_user_login(user_login: MetaDataUserLoginType) -> None:
        if not user_login:
            raise MetaDataInvalidUserLoginError(user_login)

    def __post_init__(self) -> None:
        """
        Обработка после инициализации метаданных карточки пользователя.

        Проверка на корректность метаданных карточки пользователя.
        Генерация ID карточки пользователя.
        """
        self.__check_empty_title(self._title)
        self.__check_incorrect_icon_path(self._icon_path)
        self.__check_empty_user_login(self._user_login)

        self.__card_id = self.__generate_card_id()

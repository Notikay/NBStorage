from __future__ import annotations

import secrets
import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from domain.interfaces import CardMetaEntityInterface
from .exceptions import (
    CardMetaInvalidIconPathError,
    CardMetaInvalidTitleError,
    CardMetaInvalidUserLoginError
)
from ..mixins import UpdateEntityParamMixin

if TYPE_CHECKING:
    from domain.interfaces.card.types import (
        CardMetaTitleType,
        CardMetaIconPathType,
        CardMetaUserLoginType,
        CardMetaKeyType,
        CardMetaCardIDType,
        CardMetaUpdTitleType,
        CardMetaUpdIconPathType
    )
    from .dto import CardMetaDTO


@dataclass(slots=True)
class CardMeta(UpdateEntityParamMixin, CardMetaEntityInterface):
    """Метаданные карточки пользователя."""
    _title: CardMetaTitleType
    _icon_path: CardMetaIconPathType
    _user_login: CardMetaUserLoginType

    __key: CardMetaKeyType = field(
        default_factory=lambda: secrets.token_bytes(32),
        init=True,
        repr=False
    )
    __card_id: CardMetaCardIDType = field(init=False)

    # Поддерживаемые расширения иконок карточки пользователя.
    __ICON_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.ico', '.icon'}

    @property
    def user_login(self) -> CardMetaUserLoginType:
        """
        Логина пользователя, которому принадлежит карточка.

        Только для чтения.

        :rtype: CardMetaUserLoginType
        """
        return self._user_login

    @property
    def key(self) -> CardMetaKeyType:
        """
        Ключ шифрования данных карточки пользователя.

        Только для чтения.

        :rtype: CardMetaKeyType
        """
        return self.__key

    @property
    def card_id(self) -> CardMetaCardIDType:
        """
        ID карточки пользователя.

        Только для чтения.

        :rtype: CardMetaCardIDType
        """
        return self.__card_id

    @property
    def title(self) -> CardMetaTitleType:
        """
        Название карточки пользователя.

        Запись произойдет только в случае если новое название карточки
        не является None и будет корректным.

        :rtype: CardMetaTitleType
        """
        return self._title

    @title.setter
    def title(self, value: CardMetaUpdTitleType) -> None:
        self._update_field('_title', value, self.__check_empty_title)

    @property
    def icon_path(self) -> CardMetaIconPathType:
        """
        Путь к иконке карточки пользователя.

        Запись произойдет только в случае если новый путь к иконке
        карточки пользователя не является None и будет корректным.

        :rtype: CardMetaIconPathType
        """
        return self._icon_path

    @icon_path.setter
    def icon_path(self, value: CardMetaUpdIconPathType) -> None:
        self._update_field(
            '_icon_path',
            value,
            self.__check_incorrect_icon_path
        )

    def generate_card_id(self) -> None:
        """Генерация ID карточки пользователя."""
        self.__card_id = self.generate_uuid_from_login_and_key(
            self._user_login,
            self.__key
        )

    def to_dict(self) -> CardMetaDTO:
        """
        Преобразование в словарь.

        Путь к иконке и ID карточки пользователя преобразуются в строки.

        :return: Словарь с метаданными карточки пользователя.
        :rtype: CardMetaDTO
        """
        return {
            'title': self._title,
            'icon_path': str(self._icon_path),
            'user_login': self._user_login,
            'card_id': str(self.__card_id)
        }

    @staticmethod
    def generate_uuid_from_login_and_key(login: str, key: bytes) -> uuid.UUID:
        """
        Генерация UUID по логину и ключу шифрования.

        :param login: Логин.
        :type login: str

        :param key: Ключ шифрования.
        :type key: bytes

        :return: UUID.
        :rtype: uuid.UUID
        """
        return uuid.uuid5(uuid.NAMESPACE_OID, name=f"{login}-{key.hex()}")

    @classmethod
    def __check_incorrect_icon_path(
            cls,
            icon_path: CardMetaIconPathType
    ) -> None:
        if icon_path.suffix.lower() not in cls.__ICON_EXTS:
            raise CardMetaInvalidIconPathError(icon_path)

    @staticmethod
    def __check_empty_title(title: CardMetaTitleType) -> None:
        if not title:
            raise CardMetaInvalidTitleError(title)

    @staticmethod
    def __check_empty_user_login(user_login: CardMetaUserLoginType) -> None:
        if not user_login:
            raise CardMetaInvalidUserLoginError(user_login)

    def __post_init__(self) -> None:
        """
        Обработка после инициализации метаданных карточки пользователя.

        Проверка на корректность метаданных карточки пользователя.
        Генерация ID карточки пользователя.
        """
        self.__check_empty_title(self._title)
        self.__check_incorrect_icon_path(self._icon_path)
        self.__check_empty_user_login(self._user_login)

        self.generate_card_id()

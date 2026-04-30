from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from domain.interfaces import UserMetaEntityInterface
from .exceptions import (
    UserMetaInvalidAvatarPathError,
    UserMetaInvalidNameError,
    UserMetaInvalidTimeBlockError
)
from ..mixins import UpdateEntityParamMixin

if TYPE_CHECKING:
    from domain.interfaces.user.types import (
        UserMetaNameType,
        UserMetaAvatarPathType,
        UserMetaTimeBlockType,
        UserMetaSaltType,
        UserMetaUpdNameType,
        UserMetaUpdAvatarPathType,
        UserMetaUpdTimeBlockType
    )
    from .dto import UserMetaDTO


@dataclass(slots=True)
class UserMeta(UpdateEntityParamMixin, UserMetaEntityInterface):
    """Метаданные пользователя."""
    _name: UserMetaNameType
    _avatar_path: UserMetaAvatarPathType
    _time_block: UserMetaTimeBlockType

    __salt: UserMetaSaltType = field(
        default_factory=lambda: secrets.token_bytes(16),
        init=True,
        repr=False
    )

    # Поддерживаемые расширения аватарок пользователя.
    __ICON_EXTS = {'.png', '.jpg', '.jpeg', '.webp'}

    @property
    def salt(self) -> UserMetaSaltType:
        """
        Соль хеширования пароля пользователя.

        Только для чтения.

        :rtype: UserMetaSaltType
        """
        return self.__salt

    @property
    def name(self) -> UserMetaNameType:
        """
        Имя пользователя.

        Запись произойдет только в случае если новое имя пользователя
        не является None и будет корректным.

        :rtype: UserMetaNameType
        """
        return self._name

    @name.setter
    def name(self, value: UserMetaUpdNameType) -> None:
        self._update_field('_name', value, self.__check_empty_name)

    @property
    def avatar_path(self) -> UserMetaAvatarPathType:
        """
        Путь к аватарке пользователя.

        Запись произойдет только в случае если новый путь к аватарке
        пользователя не является None и будет корректным.

        :rtype: UserMetaAvatarPathType
        """
        return self._avatar_path

    @avatar_path.setter
    def avatar_path(self, value: UserMetaUpdAvatarPathType) -> None:
        self._update_field(
            '_avatar_path',
            value,
            self.__check_incorrect_avatar_path
        )

    @property
    def time_block(self) -> UserMetaTimeBlockType:
        """
        Время блокировки сессии пользователя.

        Запись произойдет только в случае если новое время блокировки
        сессии пользователя не является None и будет корректным.

        :rtype: UserMetaTimeBlockType
        """
        return self._time_block

    @time_block.setter
    def time_block(self, value: UserMetaUpdTimeBlockType) -> None:
        self._update_field(
            '_time_block',
            value,
            self.__check_negative_time_block
        )

    def to_dict(self) -> UserMetaDTO:
        """
        Преобразование в словарь.

        Путь к аватарке пользователя преобразуется в строку.

        :return: Словарь с метаданными пользователя.
        :rtype: UserMetaDTO
        """
        return {
            'name': self._name,
            'avatar_path': str(self._avatar_path),
            'time_block': self._time_block
        }

    @classmethod
    def __check_incorrect_avatar_path(
            cls,
            avatar_path: UserMetaAvatarPathType
    ) -> None:
        if avatar_path.suffix.lower() not in cls.__ICON_EXTS:
            raise UserMetaInvalidAvatarPathError(avatar_path)

    @staticmethod
    def __check_empty_name(name: UserMetaNameType) -> None:
        if not name:
            raise UserMetaInvalidNameError(name)

    @staticmethod
    def __check_negative_time_block(time_block: UserMetaTimeBlockType) -> None:
        if time_block < 0:
            raise UserMetaInvalidTimeBlockError(time_block)

    def __post_init__(self) -> None:
        """
        Обработка после инициализации метаданных пользователя.

        Проверка на корректность метаданных пользователя.
        """
        self.__check_empty_name(self._name)
        self.__check_incorrect_avatar_path(self._avatar_path)
        self.__check_negative_time_block(self._time_block)

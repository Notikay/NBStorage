from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from domain.interfaces import AbstractEntity
from .dto import SettingsDTO
from .exceptions import (
    SettingsInvalidAvatarPathError,
    SettingsInvalidNameError,
    SettingsInvalidTimeBlockError
)

if TYPE_CHECKING:
    from domain.interfaces.units.user.user_types import (
        SettingsNameType,
        SettingsAvatarPathType,
        SettingsTimeBlockType,
        SettingsUpdNameType,
        SettingsUpdAvatarPathType,
        SettingsUpdTimeBlockType
    )


@dataclass(slots=True)
class Settings(AbstractEntity[SettingsDTO]):
    """
    Настройки пользователя.

    :var _name: Атрибут имени пользователя.
    :type _name: SettingsNameType

    :var _avatar_path: Атрибут пути к аватарке пользователя.
    :type _avatar_path: SettingsAvatarPathType

    :var _time_block: Атрибут времени блокировки сессии пользователя.
    :type _time_block: SettingsTimeBlockType

    :cvar __ICON_EXTS: Атрибут поддерживаемых расширений аватарок
                       пользователя.
    :type __ICON_EXTS: set[str]
    """
    _name: SettingsNameType
    _avatar_path: SettingsAvatarPathType
    _time_block: SettingsTimeBlockType

    __ICON_EXTS = {'.png', '.jpg', '.jpeg', '.webp'}

    @property
    def name(self) -> SettingsNameType:
        return self._name

    @name.setter
    def name(self, value: SettingsUpdNameType) -> None:
        self._update_field('_name', value, self.__check_empty_name)

    @property
    def avatar_path(self) -> SettingsAvatarPathType:
        return self._avatar_path

    @avatar_path.setter
    def avatar_path(self, value: SettingsUpdAvatarPathType) -> None:
        self._update_field(
            '_avatar_path',
            value,
            self.__check_incorrect_avatar_path
        )

    @property
    def time_block(self) -> SettingsTimeBlockType:
        return self._time_block

    @time_block.setter
    def time_block(self, value: SettingsUpdTimeBlockType) -> None:
        self._update_field(
            '_time_block',
            value,
            self.__check_negative_time_block
        )

    def to_dict(self) -> SettingsDTO:
        """
        Преобразование в словарь.

        Путь к аватарке пользователя преобразуется в строку.

        :return: Словарь с настройками пользователя.
        :rtype: SettingsDTO
        """
        return {
            'name': self._name,
            'avatar_path': str(self._avatar_path),
            'time_block': self._time_block
        }

    @classmethod
    def __check_incorrect_avatar_path(
            cls,
            avatar_path: SettingsAvatarPathType
    ) -> None:
        if avatar_path.suffix.lower() not in cls.__ICON_EXTS:
            raise SettingsInvalidAvatarPathError(avatar_path)

    @staticmethod
    def __check_empty_name(name: SettingsNameType) -> None:
        if not name:
            raise SettingsInvalidNameError(name)

    @staticmethod
    def __check_negative_time_block(time_block: SettingsTimeBlockType) -> None:
        if time_block < 0:
            raise SettingsInvalidTimeBlockError(time_block)

    def __post_init__(self) -> None:
        """
        Обработка после инициализации настроек пользователя.

        Проверка на корректность настроек пользователя.
        """
        self.__check_empty_name(self._name)
        self.__check_incorrect_avatar_path(self._avatar_path)
        self.__check_negative_time_block(self._time_block)

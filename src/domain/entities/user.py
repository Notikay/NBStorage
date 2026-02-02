from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from hashlib import pbkdf2_hmac
from typing import TYPE_CHECKING, TypedDict

from ..interfaces import AbstractData

if TYPE_CHECKING:
    from pathlib import Path


class SettingsDTO(TypedDict):
    name: str
    avatar_path: str
    time_block: int


class UserDTO(TypedDict):
    login: str
    settings: SettingsDTO


@dataclass(slots=True)
class Settings(AbstractData[SettingsDTO]):
    """Настройки пользователя."""

    _name: str
    _avatar_path: Path
    _time_block: int

    __ICON_EXTS = {'.png', '.jpg', '.jpeg', '.webp'}

    @property
    def name(self) -> str:
        return self._name

    @property
    def avatar_path(self) -> Path:
        return self._avatar_path

    @property
    def time_block(self) -> float:
        return self._time_block

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

    def __post_init__(self) -> None:
        """
        Обработка после инициализации настроек пользователя.

        Проверка на корректность настроек пользователя.
        Генерация ID карточки пользователя.

        :raises ValueError: Если имя пользователя пустое.
                            Если аватарка пользователя имеет неподдерживаемый
                            формат.
                            Если время блокировки отрицательное.
        """
        if not self._name:
            raise ValueError("Имя пользователя не должно быть пустым!")
        elif self._avatar_path.suffix.lower() not in self.__ICON_EXTS:
            raise ValueError("Аватарка пользователя имеет неподдерживаемый "
                             "формат!")
        elif self._time_block < 0:
            raise ValueError("Время блокировки не может быть отрицательным!")


@dataclass(slots=True)
class User(AbstractData[UserDTO]):
    """Пользователь."""

    _login: str
    _password: bytes = field(repr=False)
    _settings: Settings

    __salt: bytes = field(
        default_factory=lambda: secrets.token_bytes(16),
        init=False,
        repr=False
    )

    @property
    def login(self) -> str:
        return self._login

    @property
    def password(self) -> bytes:
        return self._password

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def salt(self) -> bytes:
        return self.__salt

    def to_dict(self) -> UserDTO:
        """
        Преобразование в словарь.

        Пароль в словарь не включается.

        :return: Словарь с данными пользователя.
        :rtype: UserDTO
        """
        return {
            'login': self._login,
            'settings': self._settings.to_dict()
        }

    @staticmethod
    def sha512_hash_password(
            password: bytes,
            salt: bytes,
            iterations: int = 210_000,
            length: int = 32
    ) -> bytes:
        """
        Хеширование пароля с помощью алгоритма PBKDF2-HMAC с методом
        SHA512.

        По-умолчанию используется 210000 итераций хеширования и 32
        байта для длины хеша.

        :param password: Пароль, который нужно хешировать.
        :type password: bytes

        :param salt: Соль для хеширования.
        :type salt: bytes

        :param iterations: Количество итераций хеширования.
        :type iterations: int

        :param length: Длина хеша.
        :type length: int

        :return: Хешированный пароль.
        :rtype: bytes
        """
        return pbkdf2_hmac(
            'sha512',
            password,
            salt,
            iterations,
            length
        )

    def __post_init__(self) -> None:
        """
        Обработка после инициализации пользователя.

        Проверка на корректность пользователя.
        Хеширование пароля.

        :raises ValueError: Если логин или пароль пользователя пустые.
        """

        if not self._login:
            raise ValueError("Логин пользователя не должен быть пустым!")
        elif not self._password:
            raise ValueError("Пароль пользователя не должен быть пустым!")

        self._password = self.sha512_hash_password(self._password, self.__salt)

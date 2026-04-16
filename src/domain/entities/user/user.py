from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from hashlib import pbkdf2_hmac
from typing import TYPE_CHECKING

from domain.interfaces.units.user import UserEntityInterface
from .dto import UserDTO
from .exceptions import UserInvalidLoginError, UserInvalidPasswordError

if TYPE_CHECKING:
    from domain.interfaces.units.user.user_types import (
        UserLoginType,
        UserPasswordType
    )
    from .settings import Settings


@dataclass(slots=True)
class User(UserEntityInterface[UserDTO]):
    """
    Пользователь.

    :var _settings: Атрибут настроек пользователя.
    :type _settings: Settings

    :var _login: Атрибут логина пользователя.
    :type _login: UserLoginType

    :var _password: Атрибут пароля пользователя.
    :type _password: UserPasswordType

    :var __salt: Атрибут соли для хеширования пароля пользователя.
    :type __salt: bytes
    """
    _settings: Settings
    _login: UserLoginType
    _password: UserPasswordType = field(repr=False)

    __salt: bytes = field(
        default_factory=lambda: secrets.token_bytes(16),
        init=True,
        repr=False
    )

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def login(self) -> UserLoginType:
        return self._login

    @property
    def salt(self) -> bytes:
        return self.__salt

    @property
    def password(self) -> UserPasswordType:
        return self._password

    @password.setter
    def password(self, value: UserPasswordType) -> None:
        self.__check_password(value)
        self._password = value

    def hash_password(self) -> None:
        """Хеширование пароля."""
        self._password = self.sha512_hash_password(self._password, self.__salt)

    def to_dict(self) -> UserDTO:
        """
        Преобразование в словарь.

        Пароль в словарь не включается.

        :return: Словарь с данными пользователя.
        :rtype: UserDTO
        """
        return {
            'settings': self._settings.to_dict(),
            'login': self._login
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

    @staticmethod
    def __check_login(login: UserLoginType) -> None:
        if not login:
            raise UserInvalidLoginError(login)

    @staticmethod
    def __check_password(password: UserPasswordType) -> None:
        if not password:
            raise UserInvalidPasswordError(password)

    def __post_init__(self) -> None:
        """
        Обработка после инициализации пользователя.

        Проверка на корректность пользователя.
        """
        self.__check_login(self._login)
        self.__check_password(self._password)

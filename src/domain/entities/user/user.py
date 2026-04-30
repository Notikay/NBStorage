from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import pbkdf2_hmac
from typing import TYPE_CHECKING

from domain.interfaces import UserEntityInterface
from .exceptions import UserInvalidLoginError, UserInvalidPasswordError

if TYPE_CHECKING:
    from domain.interfaces.user.types import UserLoginType, UserPasswordType
    from .dto import UserDTO
    from .meta import UserMeta


@dataclass(slots=True)
class User(UserEntityInterface):
    """Пользователь."""
    _meta: UserMeta
    _login: UserLoginType
    _password: UserPasswordType = field(repr=False)

    @property
    def meta(self) -> UserMeta:
        """
        Метаданные пользователя.

        Только для чтения.

        :rtype: UserMeta
        """
        return self._meta

    @property
    def login(self) -> UserLoginType:
        """
        Логин пользователя.

        Только для чтения.

        :rtype: UserLoginType
        """
        return self._login

    @property
    def password(self) -> UserPasswordType:
        """
        Пароль пользователя.

        Запись произойдет только в случае если новый пароль
        пользователя не является None и будет корректным.

        :rtype: UserPasswordType
        """
        return self._password

    @password.setter
    def password(self, value: UserPasswordType) -> None:
        self.__check_password(value)
        self._password = value

    def hash_password(self) -> None:
        """Хеширование пароля."""
        self._password = self.sha512_hash_password(
            self._password,
            self.meta.salt
        )

    def to_dict(self) -> UserDTO:
        """
        Преобразование в словарь.

        Без пароля.

        :return: Словарь с данными пользователя.
        :rtype: UserDTO
        """
        return {'meta': self._meta.to_dict(), 'login': self._login}

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

        :param salt: Соль хеширования.
        :type salt: bytes

        :param iterations: Количество итераций хеширования.
        :type iterations: int

        :param length: Длина хеша.
        :type length: int

        :return: Хеш пароля.
        :rtype: bytes
        """
        return pbkdf2_hmac('sha512', password, salt, iterations, length)

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

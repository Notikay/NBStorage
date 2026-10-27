from dataclasses import dataclass, field
from hashlib import pbkdf2_hmac

from ..mixins import UpdateEntityParamMixin
from .exceptions import UserInvalidLoginError, UserInvalidPasswordError
from .meta import UserMeta
from .types import (
    UserLoginType,
    UserPasswordType,
    UserUpdLoginType,
    UserUpdPasswordType,
)


@dataclass(slots=True)
class User(UpdateEntityParamMixin):
    """Пользователь."""
    _meta: UserMeta
    _login: UserLoginType
    _password: UserPasswordType = field(repr=False)

    @property
    def meta(self) -> UserMeta:
        """
        Метаданные пользователя.

        Только для чтения.
        """
        return self._meta

    @property
    def login(self) -> UserLoginType:
        """
        Логин пользователя.

        Запись произойдет только в случае если новый логин
        пользователя не является None и будет корректным.
        """
        return self._login

    @login.setter
    def login(self, value: UserUpdLoginType) -> None:
        self._update_field('_login', value, self.__check_login)

    @property
    def password(self) -> UserPasswordType:
        """
        Пароль пользователя.

        Запись произойдет только в случае если новый пароль
        пользователя не является None и будет корректным.
        """
        return self._password

    @password.setter
    def password(self, value: UserUpdPasswordType) -> None:
        self._update_field('_password', value, self.__check_password)

    def hash_password(self) -> None:
        """Хеширование пароля."""
        self._password = self.sha512_hash_password(self._password, self.meta.salt)

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
        """Проверка логина и пароля пользователя на корректность."""
        self.__check_login(self._login)
        self.__check_password(self._password)

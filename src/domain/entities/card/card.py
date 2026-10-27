from dataclasses import dataclass, field, fields
from functools import partial
from math import ceil
from typing import Self

from .exceptions import CardInvalidParamError
from .meta import CardMeta
from .types import CardParamIsThereType, CardParamType, CardUpdParamType


@dataclass(slots=True)
class Card:
    """Карточка пользователя."""
    _meta: CardMeta
    _username: CardParamType
    _email: CardParamType = field(repr=False)
    _password: CardParamType = field(repr=False)
    _url: CardParamType
    _description: CardParamType

    _is_encrypted: bool = field(default=False, init=True, repr=True)

    @property
    def meta(self) -> CardMeta:
        """
        Метаданные карточки пользователя.

        Только для чтения.
        """
        return self._meta

    @property
    def is_encrypted(self) -> bool:
        """
        Флаг шифровки данных карточки пользователя.

        Только для чтения.
        """
        return self._is_encrypted

    @property
    def username(self) -> CardParamType:
        """
        Имя пользователя от сервиса.

        Запись произойдет только в случае если новое имя пользователя в
        сервисе не является None и будет корректным.
        """
        return self._username

    @username.setter
    def username(self, value: CardUpdParamType) -> None:
        self._update_field('_username', value)

    @property
    def email(self) -> CardParamType:
        """
        Электронная почта привязанная к сервису.

        Запись произойдет только в случае если новая электронная почта,
        привязанная к сервису, не является None и будет корректным.
        """
        return self._email

    @email.setter
    def email(self, value: CardUpdParamType) -> None:
        self._update_field('_email', value)

    @property
    def password(self) -> CardParamType:
        """
        Пароль от сервиса.

        Запись произойдет только в случае если новый пароль от сервиса
        не является None и будет корректным.
        """
        return self._password

    @password.setter
    def password(self, value: CardUpdParamType) -> None:
        self._update_field('_password', value)

    @property
    def url(self) -> CardParamType:
        """
        URL-адрес сервиса.

        Запись произойдет только в случае если новый URL-адрес сервиса
        не является None и будет корректным.
        """
        return self._url

    @url.setter
    def url(self, value: CardUpdParamType) -> None:
        self._update_field('_url', value)

    @property
    def description(self) -> CardParamType:
        """
        Описание сервиса.

        Запись произойдет только в случае если новое описание сервиса
        не является None и будет корректным.
        """
        return self._description

    @description.setter
    def description(self, value: CardUpdParamType) -> None:
        self._update_field('_description', value)

    def encrypt(self) -> None:
        """Шифровка данных карточки пользователя."""
        encrypt_partial = partial(self.xor_otp_encrypt, key=self._meta.key)

        self._username = encrypt_partial(self._username)
        self._email = encrypt_partial(self._email)
        self._password = encrypt_partial(self._password)
        self._url = encrypt_partial(self._url)
        self._description = encrypt_partial(self._description)

        self._is_encrypted = True

    def decrypt(self) -> None:
        """Расшифровка данных карточки пользователя."""
        self.encrypt()  # toggle из-за метода шифровки (XOR OTP).
        self._is_encrypted = False

    @staticmethod
    def xor_otp_encrypt(param: bytes | None, key: bytes) -> CardParamType:
        """
        Шифровка параметра с помощью ключа, методом XOR OTP.

        Если параметр является None, то и результат шифровки будет None.
        """
        if param is None:
            return None
        if (key_mult := ceil(len(param) / len(key))) != 1:
            key *= key_mult

        return bytes(p ^ k for p, k in zip(param, key))  # noqa: B905

    def _update_field(self, param_field_name: str, value: CardUpdParamType) -> None:
        """
        Обновление параметра в карточке пользователя.

        Если параметр пуст, то он будет обновлен на None.
        Если данные карточки пользователя зашифрованы, то сначала будет
        их расшифровка, затем обновление параметра и снова шифровка.
        """
        if value is not None:
            try:
                self.__check_empty_param(value, param_field_name)
            except CardInvalidParamError:
                setattr(self, param_field_name, None)
            else:
                self.__check_param_equal_key(value, param_field_name)
                self.__check_key_must_not_start_with_param(value, param_field_name)
                if self._is_encrypted:
                    self.decrypt()
                    setattr(self, param_field_name, value)
                    self.encrypt()
                else:
                    setattr(self, param_field_name, value)

    def __check_param_equal_key(
            self,
            param: CardParamIsThereType,
            param_field_name: str
    ) -> None:
        if param == self._meta.key:
            raise CardInvalidParamError(
                param,
                param_field_name,
                "Параметр и ключ не должны быть одинаковыми!"
            )

    def __check_key_must_not_start_with_param(
            self,
            param: CardParamIsThereType,
            param_field_name: str
    ) -> None:
        if self._meta.key.startswith(param):
            raise CardInvalidParamError(
                param,
                param_field_name,
                "Ключ не должен начинаться с параметра!"
            )

    @staticmethod
    def __check_empty_param(param: CardParamIsThereType, param_field_name: str) -> None:
        if not param.replace(b'\x00', b''):
            raise CardInvalidParamError(
                param,
                param_field_name,
                "Параметр не должен быть пустым!"
            )

    def __post_init__(self: Self) -> None:
        """
        Проверка параметров на корректность.

        Параметр с метаданными карточки пользователя (_metadata) и флаг
        шифровки данных карточки пользователя (_is_encrypted) не
        проверяются.
        """
        for param_field in fields(self):
            if param_field.name in ('_meta', '_is_encrypted'):
                continue
            if (param := getattr(self, param_field.name)) is not None:
                self.__check_empty_param(param, param_field.name)
                self.__check_param_equal_key(param, param_field.name)
                self.__check_key_must_not_start_with_param(param, param_field.name)

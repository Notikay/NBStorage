from __future__ import annotations

from dataclasses import dataclass, field, fields
from functools import partial
from math import ceil
from typing import TYPE_CHECKING, Self

from domain.interfaces import CardEntityInterface
from .exceptions import CardInvalidParamError

if TYPE_CHECKING:
    from domain.interfaces.card.types import (
        CardParamType,
        CardUpdParamType,
        CardParamIsThereType
    )
    from .dto import CardDTO
    from .meta import CardMeta


@dataclass(slots=True)
class Card(CardEntityInterface):
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

        :rtype: CardMeta
        """
        return self._meta

    @property
    def is_encrypted(self) -> bool:
        """
        Флаг шифровки данных карточки пользователя.

        Только для чтения.

        :rtype: bool
        """
        return self._is_encrypted

    @property
    def username(self) -> CardParamType:
        """
        Имя пользователя от сервиса.

        Запись произойдет только в случае если новое имя пользователя в
        сервисе не является None и будет корректным.

        :rtype: CardParamType
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

        :rtype: CardParamType
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

        :rtype: CardParamType
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

        :rtype: CardParamType
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

        :rtype: CardParamType
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
        self.encrypt()  # toggle из-за метода шифровки (XOR OTP)
        self._is_encrypted = False

    def to_dict(self) -> CardDTO:
        """
        Преобразование в словарь.

        Проверка на шифрованные данные карточки пользователя, для
        корректного преобразования в словарь.

        :return: Словарь с данными карточки пользователя.
        :rtype: CardDTO
        """
        if self._is_encrypted:
            username = self._username.hex() \
                if self._username is not None else None
            email = self._email.hex() \
                if self._email is not None else None
            password = self._password.hex() \
                if self._password is not None else None
            url = self._url.hex() \
                if self._url is not None else None
            description = self._description.hex() \
                if self._description is not None else None
        else:
            username = self._username.decode('utf-8') \
                if self._username is not None else None
            email = self._email.decode('utf-8') \
                if self._email is not None else None
            password = self._password.decode('utf-8') \
                if self._password is not None else None
            url = self._url.decode('utf-8') \
                if self._url is not None else None
            description = self._description.decode('utf-8') \
                if self._description is not None else None

        return {
            'meta': self._meta.to_dict(),
            'username': username,
            'email': email,
            'password': password,
            'url': url,
            'description': description
        }

    @staticmethod
    def xor_otp_encrypt(param: bytes | None, key: bytes) -> CardParamType:
        """
        Шифровка параметра методом XOR OTP.

        Если параметр является None, то и результат шифровки этого
        параметра будет None, несмотря на ключ.

        :param param: Параметр, который нужно зашифровать.
        :type param: bytes | None

        :param key: Ключ шифровки.
        :type key: bytes

        :return: Зашифрованный параметр.
        :rtype: CardParamType
        """
        if param is None:
            return None
        if (key_mult := ceil(len(param) / len(key))) != 1:
            key *= key_mult

        return bytes(p ^ k for p, k in zip(param, key))

    def _update_field(
            self,
            param_field_name: str,
            value: CardUpdParamType
    ) -> None:
        """
        Обновление параметра в карточке пользователя.

        Если параметр пуст, то он будет обновлен на None.
        Если данные карточки пользователя зашифрованы, то сначала будет
        их расшифровка, затем обновление параметра и снова шифровка.

        :param param_field_name: Название параметра в карточке
                                 пользователя.
        :type param_field_name: str

        :param value: Новое значение параметра в карточке пользователя.
        :type value: CardUpdParamType
        """
        if value is not None:
            try:
                self.__check_empty_param(value, param_field_name)
            except CardInvalidParamError:
                setattr(self, param_field_name, None)
            else:
                self.__check_param_equal_key(value, param_field_name)
                self.__check_key_must_not_start_with_param(
                    value,
                    param_field_name
                )
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
    ):
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
    ):
        if self._meta.key.startswith(param):
            raise CardInvalidParamError(
                param,
                param_field_name,
                "Ключ не должен начинаться с параметра!"
            )

    @staticmethod
    def __check_empty_param(
            param: CardParamIsThereType,
            param_field_name: str
    ):
        if not param.replace(b'\x00', b''):
            raise CardInvalidParamError(
                param,
                param_field_name,
                "Параметр не должен быть пустым!"
            )


    def __post_init__(self: Self) -> None:
        """
        Обработка после инициализации карточки пользователя.

        Проверка на корректность данных карточки пользователя.
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
                self.__check_key_must_not_start_with_param(
                    param,
                    param_field.name
                )

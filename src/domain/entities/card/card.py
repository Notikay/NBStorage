from __future__ import annotations

from dataclasses import dataclass, field, fields
from functools import partial
from math import ceil
from typing import TYPE_CHECKING, override, Self

from domain.interfaces.units.card import CardEntityInterface
from .dto import CardDTO
from .exceptions import CardInvalidParamFieldError

if TYPE_CHECKING:
    from domain.interfaces.units.card.card_types import (
        CardParamType,
        CardUpdParamType
    )
    from domain.interfaces.base.base_types import CheckParamFnType
    from .metadata import MetaData


@dataclass(slots=True)
class Card(CardEntityInterface[CardDTO]):
    """
    Карточка пользователя.

    :var _metadata: Атрибут метаданных карточки пользователя.
    :type _metadata: MetaData

    :var _username: Атрибут имени пользователя от сервиса.
    :type _username: CardParamType

    :var _email: Атрибут электронной почты привязанный к сервису.
    :type _email: CardParamType

    :var _password: Атрибут пароля от сервиса.
    :type _password: CardParamType

    :var _url: Атрибут URL-адреса сервиса.
    :type _url: CardParamType

    :var _description: Атрибут описания сервиса.
    :type _description: CardParamType

    :var _is_encrypted: Атрибут флага шифровки данных для карточки
                        пользователя.
    :type _is_encrypted: bool
    """
    _metadata: MetaData
    _username: CardParamType
    _email: CardParamType = field(repr=False)
    _password: CardParamType = field(repr=False)
    _url: CardParamType
    _description: CardParamType

    _is_encrypted: bool = field(default=False, init=True, repr=False)

    @property
    def metadata(self) -> MetaData:
        return self._metadata

    @property
    def is_encrypted(self) -> bool:
        return self._is_encrypted

    @property
    def username(self) -> CardParamType:
        return self._username

    @username.setter
    def username(self, value: CardUpdParamType) -> None:
        self._update_field('_username', value)

    @property
    def email(self) -> CardParamType:
        return self._email

    @email.setter
    def email(self, value: CardUpdParamType) -> None:
        self._update_field('_email', value)

    @property
    def password(self) -> CardParamType:
        return self._password

    @password.setter
    def password(self, value: CardUpdParamType) -> None:
        self._update_field('_password', value)

    @property
    def url(self) -> CardParamType:
        return self._url

    @url.setter
    def url(self, value: CardUpdParamType) -> None:
        self._update_field('_url', value)

    @property
    def description(self) -> CardParamType:
        return self._description

    @description.setter
    def description(self, value: CardUpdParamType) -> None:
        self._update_field('_description', value)

    def encrypt(self) -> None:
        """Шифровка данных карточки пользователя."""
        encrypt_partial = partial(self.xor_otp_encrypt, key=self._metadata.key)

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

        Проверка на шифрованность данных карточки пользователя, для
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
            'metadata': self._metadata.to_dict(),
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

    @override
    def _update_field(
            self,
            param_field_name: str,
            value: CardUpdParamType,
            check_param_fn: CheckParamFnType | None = None
    ) -> None:
        """
        Обновление параметра в данных карточки пользователя.

        Если параметр пуст, то он будет обновлен на None.
        Если данные карточки пользователя зашифрованы, то сначала будет
        их расшифровка, затем обновление параметра и снова шифровка.

        :param param_field_name: Название параметра в данных карточки
                                 пользователя.
        :type param_field_name: str

        :param value: Новое значение параметра в данных карточки
                      пользователя.
        :type value: CardUpdParamType

        :param check_param_fn: Функция проверки корректности параметра
                               в данных карточки пользователя.
                               Не используется в текущей реализации.
        :type check_param_fn: CheckParamFnType | None
        """
        if value is not None:
            if value.replace(b'\x00', b''):
                if self._is_encrypted:
                    self.decrypt()
                    setattr(self, param_field_name, value)
                    self.encrypt()
                else:
                    setattr(self, param_field_name, value)
            else:
                setattr(self, param_field_name, None)

    def __post_init__(self: Self) -> None:
        """
        Обработка после инициализации карточки пользователя.

        Проверка на корректность данных карточки пользователя.
        Параметр с метаданными карточки пользователя (_metadata) и флаг
        шифровки данных для карточки пользователя (_is_encrypted) не
        проверяются.

        :raises CardInvalidParamFieldError: Если параметр и ключ
                                            одинаковы.
                                            Если параметр пуст.
                                            Если ключ начинается с
                                            параметра.
        """
        for param_field in fields(self):
            if param_field.name in ('_metadata', '_is_encrypted'):
                continue
            if (param := getattr(self, param_field.name)) is not None:
                if param == self._metadata.key:
                    raise CardInvalidParamFieldError(
                        param,
                        param_field.name,
                        "Параметр и ключ не должны быть одинаковыми!"
                    )
                elif not param.replace(b'\x00', b''):
                    raise CardInvalidParamFieldError(
                        param,
                        param_field.name
                    )
                elif self._metadata.key.startswith(param):
                    raise CardInvalidParamFieldError(
                        param,
                        param_field.name,
                        "Ключ не должен начинаться с параметра!"
                    )

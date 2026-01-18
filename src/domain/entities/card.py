from __future__ import annotations

import secrets
import uuid
from dataclasses import dataclass, field, fields
from functools import partial
from math import ceil
from typing import TYPE_CHECKING, TypedDict

from ..interfaces import AbstractData, AbstractCard

if TYPE_CHECKING:
    from pathlib import Path

    from ..interfaces.types import ParamType


class MetaDataDTO(TypedDict):
    title: str
    icon_path: str
    user_login: str
    card_id: str


class CardDataDTO(TypedDict):
    meta: MetaDataDTO
    username: str | None
    email: str | None
    password: str | None
    url: str | None
    description: str | None


@dataclass(slots=True)
class MetaData(AbstractData):
    """Метаданные карточки пользователя."""

    _title: str
    _icon_path: Path
    _user_login: str

    __card_id: uuid.UUID = field(init=False)
    __key: bytes = field(
        default=secrets.token_bytes(32),
        init=False,
        repr=False
    )

    @property
    def title(self) -> str:
        return self._title

    @property
    def icon_path(self) -> Path:
        return self._icon_path

    @property
    def user_login(self) -> str:
        return self._user_login

    @property
    def card_id(self) -> uuid.UUID:
        return self.__card_id

    @property
    def key(self) -> bytes:
        return self.__key

    def to_dict(self) -> MetaDataDTO:
        return {
            'title': self._title,
            'icon_path': str(self._icon_path),
            'user_login': self._user_login,
            'card_id': str(self.__card_id)
        }

    def __generate_card_id(self) -> uuid.UUID:
        return uuid.uuid5(
            uuid.NAMESPACE_OID,
            name=f"{self._user_login}-{self.__key.hex()}"
        )

    def __post_init__(self) -> None:
        """
        Обработка после инициализации метаданных карточки пользователя.

        Проверка на корректность метаданных карточки пользователя.
        Генерация ID карточки пользователя.
        """
        if not self._title:
            raise ValueError("Заголовок карточки не должен быть пустым!")
        elif not self._icon_path.is_file():
            raise FileNotFoundError("Иконка карточки пользователя не найдена "
                                    f"по пути: {self._icon_path}")
        elif not self._user_login:
            raise ValueError("Логин пользователя не должен быть пустым!")

        self.__card_id = self.__generate_card_id()


@dataclass(slots=True)
class Card(AbstractCard):
    """Карточка пользователя."""

    _meta: MetaData
    _username: ParamType
    _email: ParamType = field(repr=False)
    _password: ParamType = field(repr=False)
    _url: ParamType
    _description: ParamType

    # Флаг шифровки данных карточки пользователя
    _is_encrypted: bool = field(default=False, init=False, repr=False)

    @property
    def meta(self) -> MetaData:
        return self._meta

    @property
    def username(self) -> ParamType:
        return self._username

    @property
    def email(self) -> ParamType:
        return self._email

    @property
    def password(self) -> ParamType:
        return self._password

    @property
    def url(self) -> ParamType:
        return self._url

    @property
    def description(self) -> ParamType:
        return self._description

    def encrypt(self) -> None:
        """Шифровка данных."""
        encrypt_partial = partial(self.xor_otp_encrypt, key=self._meta.key)

        self._username = encrypt_partial(self._username)
        self._email = encrypt_partial(self._email)
        self._password = encrypt_partial(self._password)
        self._url = encrypt_partial(self._url)
        self._description = encrypt_partial(self._description)

        self._is_encrypted = True

    def decrypt(self) -> None:
        """Расшифровка данных."""
        self.encrypt()  # toggle из-за метода шифровки (XOR OTP)
        self._is_encrypted = False

    def to_dict(self) -> CardDataDTO:
        """
        Преобразование в словарь.

        Проверка на шифрованность данных карточки пользователя для
        корректного преобразования в словарь.

        :return: Словарь с данными карточки пользователя.
        :rtype: CardDataDTO
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
    def xor_otp_encrypt(param: ParamType, key: bytes) -> bytes | None:
        """
        Шифровка параметра методом XOR OTP.

        Если параметр является None, то и результат шифровки этого
        параметра будет None, несмотря на ключ.

        :param param: Параметр, который нужно зашифровать.
        :type param: ParamType

        :param key: Ключ шифровки.
        :type key: bytes

        :return: Зашифрованный параметр.
        :rtype: bytes | None
        """
        if param is None: return None  # noqa: E701
        if (key_mult := ceil(len(param) / len(key))) != 1:
            key *= key_mult

        return bytes(p ^ k for p, k in zip(param, key))

    def __post_init__(self) -> None:
        """
        Обработка после инициализации карточки пользователя.

        Проверка на корректность данных карточки пользователя. Параметр
        с метаданными карточки пользователя (_meta) не проверяется.

        :raises ValueError: Если параметр и ключ одинаковы.
                            Если параметр или ключ пусты.
                            Если ключ начинается с параметра.
        """
        for param_field in fields(self):
            if param_field.name in ('_meta', '_is_encrypted'):
                continue
            if (param := getattr(self, param_field.name)) is not None:
                if param == self._meta.key:
                    raise ValueError("Параметр и ключ не должны быть "
                                     "одинаковыми!")
                elif (not param.replace(b'\x00', b'') or
                      not self._meta.key.replace(b'\x00', b'')):
                    raise ValueError("Параметр и ключ не должны быть пустыми!")
                elif self._meta.key.startswith(param):
                    raise ValueError("Ключ начинается с параметра!")

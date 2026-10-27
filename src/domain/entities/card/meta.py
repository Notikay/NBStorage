import re
import secrets
import uuid
from dataclasses import dataclass, field

from ..mixins import UpdateEntityParamMixin
from .exceptions import CardMetaInvalidIconKeyError, CardMetaInvalidTitleError
from .types import (
    CardMetaIDType,
    CardMetaIconIsThereType,
    CardMetaIconKeyType,
    CardMetaKeyType,
    CardMetaTitleType,
    CardMetaUpdTitleType,
    CardMetaUserIDType,
)


@dataclass(slots=True)
class CardMeta(UpdateEntityParamMixin):
    """Метаданные карточки пользователя."""
    _title: CardMetaTitleType
    _icon_key: CardMetaIconKeyType
    _user_id: CardMetaUserIDType

    __key: CardMetaKeyType = field(
        default_factory=secrets.token_bytes,
        init=True,
        repr=False
    )
    __card_id: CardMetaIDType = field(default=None, init=False)

    __ICON_PREFIX = "cards/icons/"
    __ICON_DEFAULT_NAME = "default"
    __ICON_EXT = "webp"
    __ICON_KEY_PATTERN = re.compile(rf"^{__ICON_PREFIX}[^/]+\.{__ICON_EXT}$")

    @property
    def user_id(self) -> CardMetaUserIDType:
        """
        ID пользователя, которому принадлежит карточка.

        Только для чтения.
        """
        return self._user_id

    @property
    def key(self) -> CardMetaKeyType:
        """
        Ключ шифрования данных карточки пользователя.

        Только для чтения.
        """
        return self.__key

    @property
    def card_id(self) -> CardMetaIDType:
        """
        ID карточки пользователя.

        Только для чтения.
        """
        return self.__card_id

    @property
    def title(self) -> CardMetaTitleType:
        """
        Название карточки пользователя.

        Запись произойдет только в случае если новое название карточки
        не является None и будет корректным.
        """
        return self._title

    @title.setter
    def title(self, value: CardMetaUpdTitleType) -> None:
        self._update_field('_title', value, self.__check_empty_title)

    @property
    def icon_key(self) -> CardMetaIconKeyType:
        """
        Ключ иконки карточки пользователя.

        Запись произойдет только в случае если новый ключ иконки
        карточки пользователя будет корректным.
        """
        return self._icon_key

    @icon_key.setter
    def icon_key(self, value: CardMetaIconKeyType) -> None:
        if value is None:
            self._icon_key = value
        else:
            self._update_field('_icon_key', value, self.__check_incorrect_icon_key)

    @classmethod
    def get_default_icon_key(cls) -> CardMetaIconIsThereType:
        return f"{cls.__ICON_PREFIX}{cls.__ICON_DEFAULT_NAME}.{cls.__ICON_EXT}"

    @staticmethod
    def generate_uuid_from_string_and_key(string: str, key: bytes) -> uuid.UUID:
        """Генерация UUID по произвольной строке и ключу шифрования."""
        return uuid.uuid5(uuid.NAMESPACE_OID, name=f"{string}-{key.hex()}")

    def _generate_card_id(self) -> None:
        """Генерация ID карточки пользователя."""
        self.__card_id = self.generate_uuid_from_string_and_key(
            self._user_id.hex,
            self.__key
        )

    @classmethod
    def __check_incorrect_icon_key(cls, icon_key: CardMetaIconKeyType) -> None:
        if (icon_key is not None) and (not cls.__ICON_KEY_PATTERN.fullmatch(icon_key)):
            raise CardMetaInvalidIconKeyError(icon_key)

    @staticmethod
    def __check_empty_title(title: CardMetaTitleType) -> None:
        if not title:
            raise CardMetaInvalidTitleError(title)

    def __post_init__(self) -> None:
        """
        Проверка названия и ключа иконки на корректность, после чего
        генерируется ID.
        """
        self.__check_empty_title(self._title)
        self.__check_incorrect_icon_key(self._icon_key)

        self._generate_card_id()

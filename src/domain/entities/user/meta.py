import re
import secrets
import uuid
from dataclasses import dataclass, field

from ..mixins import UpdateEntityParamMixin
from .exceptions import (
    UserMetaInvalidAvatarKeyError,
    UserMetaInvalidNameError,
    UserMetaInvalidTimeBlockError,
)
from .types import (
    UserMetaAvatarIsThereType,
    UserMetaAvatarKeyType,
    UserMetaIDType,
    UserMetaNameType,
    UserMetaSaltType,
    UserMetaTimeBlockType,
    UserMetaUpdNameType,
    UserMetaUpdTimeBlockType,
)


@dataclass(slots=True)
class UserMeta(UpdateEntityParamMixin):
    """Метаданные пользователя."""
    _name: UserMetaNameType
    _avatar_key: UserMetaAvatarKeyType
    _time_block: UserMetaTimeBlockType

    __salt: UserMetaSaltType = field(
        default_factory=lambda: secrets.token_bytes(16),
        init=True,
        repr=False
    )
    __user_id: UserMetaIDType = field(default=None, init=False)

    __AVATAR_PREFIX = "users/avatars/"
    __AVATAR_DEFAULT_NAME = "default"
    __AVATAR_EXT = "webp"
    __AVATAR_KEY_PATTERN = re.compile(rf"^{__AVATAR_PREFIX}[^/]+\.{__AVATAR_EXT}$")

    @property
    def salt(self) -> UserMetaSaltType:
        """
        Соль хеширования пароля пользователя.

        Только для чтения.
        """
        return self.__salt

    @property
    def user_id(self) -> UserMetaIDType:
        """
        ID пользователя.

        Только для чтения.
        """
        return self.__user_id

    @property
    def name(self) -> UserMetaNameType:
        """
        Имя пользователя.

        Запись произойдет только в случае если новое имя пользователя
        не является None и будет корректным.
        """
        return self._name

    @name.setter
    def name(self, value: UserMetaUpdNameType) -> None:
        self._update_field('_name', value, self.__check_empty_name)

    @property
    def avatar_key(self) -> UserMetaAvatarKeyType:
        """
        Ключ аватарки пользователя.

        Запись произойдет только в случае если новый ключ аватарки
        пользователя будет корректным.
        """
        return self._avatar_key

    @avatar_key.setter
    def avatar_key(self, value: UserMetaAvatarKeyType) -> None:
        if value is None:
            self._avatar_key = value
        else:
            self._update_field('_avatar_key', value, self.__check_incorrect_avatar_key)

    @property
    def time_block(self) -> UserMetaTimeBlockType:
        """
        Время блокировки сессии пользователя.

        Запись произойдет только в случае если новое время блокировки
        сессии пользователя не является None и будет корректным.
        """
        return self._time_block

    @time_block.setter
    def time_block(self, value: UserMetaUpdTimeBlockType) -> None:
        self._update_field('_time_block', value, self.__check_negative_time_block)

    @classmethod
    def get_default_avatar_key(cls) -> UserMetaAvatarIsThereType:
        return f"{cls.__AVATAR_PREFIX}{cls.__AVATAR_DEFAULT_NAME}.{cls.__AVATAR_EXT}"

    @staticmethod
    def generate_uuid_from_salt(salt: bytes) -> uuid.UUID:
        """Генерация UUID по соли."""
        return uuid.uuid5(uuid.NAMESPACE_OID, name=salt.hex())

    def _generate_user_id(self) -> None:
        """Генерация ID пользователя."""
        self.__user_id = self.generate_uuid_from_salt(self.__salt)

    @classmethod
    def __check_incorrect_avatar_key(cls, avatar_key: UserMetaAvatarKeyType) -> None:
        if (avatar_key is not None) and (
                not cls.__AVATAR_KEY_PATTERN.fullmatch(avatar_key)
        ):
            raise UserMetaInvalidAvatarKeyError(avatar_key)

    @staticmethod
    def __check_empty_name(name: UserMetaNameType) -> None:
        if not name:
            raise UserMetaInvalidNameError(name)

    @staticmethod
    def __check_negative_time_block(time_block: UserMetaTimeBlockType) -> None:
        if time_block < 0:
            raise UserMetaInvalidTimeBlockError(time_block)

    def __post_init__(self) -> None:
        """
        Проверка имени, ключа аватарки и времени блокировки сессии на
        корректность, после чего генерируется ID.
        """
        self.__check_empty_name(self._name)
        self.__check_incorrect_avatar_key(self._avatar_key)
        self.__check_negative_time_block(self._time_block)

        self._generate_user_id()

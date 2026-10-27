from shared.errors import ValidationError

from .types import (
    UserLoginType,
    UserMetaAvatarKeyType,
    UserMetaNameType,
    UserMetaTimeBlockType,
    UserPasswordType,
)


class UserMetaInvalidNameError(ValidationError):
    def __init__(self, name: UserMetaNameType) -> None:
        self.__name = name
        super().__init__(f"Некорректное имя пользователя! -> {name=}")

    @property
    def name(self) -> UserMetaNameType:
        return self.__name


class UserMetaInvalidAvatarKeyError(ValidationError):
    def __init__(self, avatar_key: UserMetaAvatarKeyType) -> None:
        self.__avatar_key = avatar_key
        super().__init__(f"Некорректный ключ аватарки пользователя! -> {avatar_key=}")

    @property
    def avatar_key(self) -> UserMetaAvatarKeyType:
        return self.__avatar_key


class UserMetaInvalidTimeBlockError(ValidationError):
    def __init__(self, time_block: UserMetaTimeBlockType) -> None:
        self.__time_block = time_block
        super().__init__(
            f"Некорректное время блокировки сессии пользователя! -> {time_block=}"
        )

    @property
    def time_block(self) -> UserMetaTimeBlockType:
        return self.__time_block


class UserInvalidLoginError(ValidationError):
    def __init__(self, login: UserLoginType) -> None:
        self.__login = login
        super().__init__(f"Некорректный логин пользователя! -> {login=}")

    @property
    def login(self) -> UserLoginType:
        return self.__login


class UserInvalidPasswordError(ValidationError):
    def __init__(self, password: UserPasswordType) -> None:
        self.__password = password
        super().__init__(f"Некорректный пароль пользователя! -> {password=!r}")

    @property
    def password(self) -> UserPasswordType:
        return self.__password

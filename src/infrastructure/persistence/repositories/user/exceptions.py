from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces.units.user.exceptions import UserRepositoryError

if TYPE_CHECKING:
    from domain.interfaces.units.user.user_types import UserLoginType


class UserCreateError(UserRepositoryError):
    """
    Ошибка создания пользователя в хранилище.

    :ivar login: Атрибут логина пользователя.
    :type login: UserLoginType
    """

    def __init__(self, login: UserLoginType):
        """
        Инициализация ошибки.

        :param login: Логин пользователя.
        :type login: UserLoginType
        """
        self.login = login

    @override
    @property
    def message(self) -> str:
        return f"Ошибка создания пользователя в хранилище! -> {self.login}"


class UserDeleteError(UserRepositoryError):
    """
    Ошибка удаления пользователя из хранилища.

    :ivar login: Атрибут логина пользователя.
    :type login: UserLoginType
    """

    def __init__(self, login: UserLoginType):
        """
        Инициализация ошибки.

        :param login: Логин пользователя.
        :type login: UserLoginType
        """
        self.login = login

    @override
    @property
    def message(self) -> str:
        return f"Ошибка удаления пользователя из хранилища! -> {self.login}"


class UserDeleteAllError(UserRepositoryError):
    """Ошибка удаления всех пользователей из хранилища."""

    @override
    @property
    def message(self) -> str:
        return "Ошибка удаления всех пользователей из хранилища!"

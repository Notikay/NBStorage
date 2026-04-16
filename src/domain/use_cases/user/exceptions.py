from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces.units.user.exceptions import UserUseCaseError

if TYPE_CHECKING:
    from domain.interfaces.units.user.user_types import UserLoginType


class UserNotFoundError(UserUseCaseError):
    """
    Ошибка при поиске пользователя.

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
        return f"Пользователь не найден! -> {self.login}"

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import User
from domain.interfaces import ChooseUserUseCaseInterface
from .exceptions import UserNotFoundError

if TYPE_CHECKING:
    from domain.interfaces import UserUnitOfWorkInterface
    from domain.interfaces.user.types import UserLoginType


class ChooseUser(ChooseUserUseCaseInterface[User]):
    """Получение пользователя."""

    def __init__(self, uow: UserUnitOfWorkInterface[User]):
        """
        Инициализация получения карточки пользователя.

        :param uow: Менеджер управления транзакцией пользователя.
        :type uow: UserUnitOfWorkInterface
        """
        self.__uow = uow

    def execute(self, login: UserLoginType) -> User:
        """
        Получение пользователя.

        :param login: Логин пользователя.
        :type login: UserLoginType

        :return: Пользователь.
        :rtype: User

        :raises UserNotFoundError: Если пользователь не найден.
        """
        with self.__uow:
            user = self.__uow.user_repos.get_item(login)
            if user is None:
                raise UserNotFoundError(login)

            self.__uow.commit()

            return user

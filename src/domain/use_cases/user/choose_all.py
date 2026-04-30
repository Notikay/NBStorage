from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import User
from domain.interfaces import ChooseAllUsersUseCaseInterface

if TYPE_CHECKING:
    from domain.interfaces import UserUnitOfWorkInterface


class ChooseAllUsers(ChooseAllUsersUseCaseInterface[User]):
    """Получение всех пользователей."""

    def __init__(self, uow: UserUnitOfWorkInterface[User]):
        """
        Инициализация получения карточки пользователя.

        :param uow: Менеджер управления транзакцией пользователя.
        :type uow: UserUnitOfWorkInterface
        """
        self.__uow = uow

    def execute(self) -> list[User]:
        """
        Получение всех пользователей.

        :return: Все пользователи.
        :rtype: list[User]
        """
        with self.__uow:
            users = list(self.__uow.user_repos.get_all_items())
            self.__uow.commit()

            return users

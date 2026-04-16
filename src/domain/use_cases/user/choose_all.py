from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.user import ChooseAllUsersUseCaseInterface
from domain.entities import User

if TYPE_CHECKING:
    from domain.interfaces.units.user import UserUnitOfWorkInterface


class ChooseAllUsers(ChooseAllUsersUseCaseInterface[User]):
    """
    Получение всех пользователей.

    :ivar __uow: Атрибут менеджера состояния транзакции пользователя.
    :type __uow: UserUnitOfWorkInterface
    """

    def __init__(self, uow: UserUnitOfWorkInterface[User]):
        """
        Инициализация получения карточки пользователя.

        :param uow: Менеджер состояния транзакции пользователя.
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
            users = self.__uow.user_repos.get_all_items()
            self.__uow.commit()

            return users

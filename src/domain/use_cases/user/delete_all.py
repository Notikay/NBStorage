from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.user import DeleteAllUsersUseCaseInterface
from domain.entities import User

if TYPE_CHECKING:
    from domain.interfaces.units.user import UserUnitOfWorkInterface


class DeleteAllUsers(DeleteAllUsersUseCaseInterface):
    """
    Удаление всех пользователей.

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

    def execute(self) -> None:
        """Удаление всех пользователей."""
        with self.__uow:
            self.__uow.user_repos.del_all_items()
            self.__uow.commit()

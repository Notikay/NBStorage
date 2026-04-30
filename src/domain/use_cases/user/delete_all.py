from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import User
from domain.interfaces import DeleteAllUsersUseCaseInterface

if TYPE_CHECKING:
    from domain.interfaces import UserUnitOfWorkInterface


class DeleteAllUsers(DeleteAllUsersUseCaseInterface):
    """Удаление всех пользователей."""

    def __init__(self, uow: UserUnitOfWorkInterface[User]):
        """
        Инициализация получения карточки пользователя.

        :param uow: Менеджер управления транзакцией пользователя.
        :type uow: UserUnitOfWorkInterface
        """
        self.__uow = uow

    def execute(self) -> None:
        """Удаление всех пользователей."""
        with self.__uow:
            self.__uow.user_repos.del_all_items()
            self.__uow.commit()

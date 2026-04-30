from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import User
from domain.interfaces import DeleteUserUseCaseInterface

if TYPE_CHECKING:
    from domain.interfaces import UserUnitOfWorkInterface
    from domain.interfaces.user.types import UserLoginType


class DeleteUser(DeleteUserUseCaseInterface):
    """Удаление пользователя."""

    def __init__(self, uow: UserUnitOfWorkInterface[User]):
        """
        Инициализация получения карточки пользователя.

        :param uow: Менеджер управления транзакцией пользователя.
        :type uow: UserUnitOfWorkInterface
        """
        self.__uow = uow

    def execute(self, login: UserLoginType) -> None:
        """
        Удаление пользователя.

        :param login: Логин пользователя.
        :type login: UserLoginType
        """
        with self.__uow:
            self.__uow.user_repos.del_item(login)
            self.__uow.commit()

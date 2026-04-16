from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.user import DeleteUserUseCaseInterface
from domain.entities import User

if TYPE_CHECKING:
    from domain.interfaces.units.user import UserUnitOfWorkInterface
    from domain.interfaces.units.user.user_types import UserLoginType


class DeleteUser(DeleteUserUseCaseInterface):
    """
    Удаление пользователя.

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

    def execute(self, login: UserLoginType) -> None:
        """
        Удаление пользователя.

        :param login: Логин пользователя.
        :type login: UserLoginType
        """
        with self.__uow:
            self.__uow.user_repos.del_item(login)
            self.__uow.commit()

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.user import ChooseUserUseCaseInterface
from domain.entities import User
from .exceptions import UserNotFoundError

if TYPE_CHECKING:
    from domain.interfaces.units.user import UserUnitOfWorkInterface
    from domain.interfaces.units.user.user_types import UserLoginType


class ChooseUser(ChooseUserUseCaseInterface[User]):
    """
    Получение пользователя.

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

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.user import ChangeUserPasswordUseCaseInterface
from domain.entities import User
from .exceptions import UserNotFoundError

if TYPE_CHECKING:
    from domain.interfaces.units.user import UserUnitOfWorkInterface
    from domain.interfaces.units.user.user_types import (
        UserLoginType,
        UserPasswordType
    )


class ChangeUserPassword(ChangeUserPasswordUseCaseInterface[User]):
    """
    Изменение пароля пользователя.

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

    def execute(
            self,
            login: UserLoginType,
            password: UserPasswordType
    ) -> User:
        """
        Изменение пароля пользователя.

        Получение пользователя из хранилища.
        Изменение пароля пользователя.
        Хеширование нового пароля пользователя.
        Обновление пользователя в хранилище.

        :param login: Логин пользователя.
        :type login: UserLoginType

        :param password: Пароль пользователя.
        :type password: UserPasswordType

        :return: Пользователь.
        :rtype: User

        :raises UserNotFoundError: Если пользователь не найден.
        """
        with self.__uow:
            user = self.__uow.user_repos.get_item(login)
            if user is None:
                raise UserNotFoundError(login)

            user.password = password
            user.hash_password()

            user = self.__uow.user_repos.upd_item(user)
            if user is None:
                raise UserNotFoundError(login)

            self.__uow.commit()

            return user

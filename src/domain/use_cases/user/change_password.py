from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import User
from domain.interfaces import ChangeUserPasswordUseCaseInterface
from .exceptions import UserNotFoundError

if TYPE_CHECKING:
    from domain.interfaces import UserUnitOfWorkInterface
    from domain.interfaces.user.types import UserLoginType, UserPasswordType


class ChangeUserPassword(ChangeUserPasswordUseCaseInterface[User]):
    """Изменение пароля пользователя."""

    def __init__(self, uow: UserUnitOfWorkInterface[User]):
        """
        Инициализация получения карточки пользователя.

        :param uow: Менеджер управления транзакцией пользователя.
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

            upd_user: User | None = self.__uow.user_repos.upd_item(user)
            if upd_user is None:
                raise UserNotFoundError(login)

            self.__uow.commit()

            return upd_user

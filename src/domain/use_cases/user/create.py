from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import User, UserMeta
from domain.interfaces import CreateUserUseCaseInterface

if TYPE_CHECKING:
    from domain.interfaces import UserUnitOfWorkInterface
    from domain.interfaces.user.types import (
        UserLoginType,
        UserPasswordType,
        UserMetaNameType,
        UserMetaAvatarPathType,
        UserMetaTimeBlockType
    )


class CreateUser(CreateUserUseCaseInterface[User]):
    """Создание пользователя."""

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
            password: UserPasswordType,
            name: UserMetaNameType,
            avatar_path: UserMetaAvatarPathType,
            time_block: UserMetaTimeBlockType
    ) -> User:
        """
        Создание пользователя.

        Формирование пользователя.
        Хеширование пароля пользователя.
        Сохранение пользователя в хранилище.

        :param login: Логин пользователя.
        :type login: UserLoginType

        :param password: Пароль пользователя.
        :type password: UserPasswordType

        :param name: Имя пользователя.
        :type name: UserMetaNameType

        :param avatar_path: Путь к аватарке пользователя.
        :type avatar_path: UserMetaAvatarPathType

        :param time_block: Время блокировки сессии пользователя.
        :type time_block: UserMetaTimeBlockType

        :return: Пользователь.
        :rtype: User
        """
        with self.__uow:
            user = User(
                UserMeta(name, avatar_path, time_block),
                login,
                password
            )
            user.hash_password()

            user = self.__uow.user_repos.set_item(user)

            self.__uow.commit()

            return user

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import User, Settings
from domain.interfaces.units.user import CreateUserUseCaseInterface

if TYPE_CHECKING:
    from domain.interfaces.units.user import UserUnitOfWorkInterface
    from domain.interfaces.units.user.user_types import (
        UserLoginType,
        UserPasswordType,
        SettingsNameType,
        SettingsAvatarPathType,
        SettingsTimeBlockType
    )


class CreateUser(CreateUserUseCaseInterface[User]):
    """
    Создание пользователя.

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
            password: UserPasswordType,
            name: SettingsNameType,
            avatar_path: SettingsAvatarPathType,
            time_block: SettingsTimeBlockType
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
        :type name: SettingsNameType

        :param avatar_path: Путь к аватарке пользователя.
        :type avatar_path: SettingsAvatarPathType

        :param time_block: Время блокировки сессии пользователя.
        :type time_block: SettingsTimeBlockType

        :return: Пользователь.
        :rtype: User
        """
        with self.__uow:
            user = User(
                Settings(name, avatar_path, time_block),
                login,
                password
            )
            user.hash_password()

            user = self.__uow.user_repos.set_item(user)

            self.__uow.commit()

            return user

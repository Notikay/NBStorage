from __future__ import annotations

from typing import TYPE_CHECKING

from domain.interfaces.units.user import UpdateSettingsUseCaseInterface
from domain.entities import User
from .exceptions import UserNotFoundError

if TYPE_CHECKING:
    from domain.interfaces.units.user import UserUnitOfWorkInterface
    from domain.interfaces.units.user.user_types import (
        UserLoginType,
        SettingsUpdNameType,
        SettingsUpdAvatarPathType,
        SettingsUpdTimeBlockType
    )


class UpdateSettings(UpdateSettingsUseCaseInterface[User]):
    """
    Обновление настроек пользователя.

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
            name: SettingsUpdNameType,
            avatar_path: SettingsUpdAvatarPathType,
            time_block: SettingsUpdTimeBlockType
    ) -> User:
        """
        Обновление настроек пользователя.

        :param login: Логин пользователя.
        :type login: UserLoginType

        :param name: Имя пользователя.
        :type name: SettingsUpdNameType

        :param avatar_path: Путь к аватарке пользователя.
        :type avatar_path: SettingsUpdAvatarPathType

        :param time_block: Время блокировки сессии пользователя.
        :type time_block: SettingsUpdTimeBlockType

        :return: Пользователь.
        :rtype: User

        :raises UserNotFoundError: Если пользователь не найден.
        """
        with self.__uow:
            user = self.__uow.user_repos.get_item(login)
            if user is None:
                raise UserNotFoundError(login)

            # Mypy ругается на разные типы для property и setter
            user.settings.name = name  # type: ignore
            user.settings.avatar_path = avatar_path  # type: ignore
            user.settings.time_block = time_block  # type: ignore

            user = self.__uow.user_repos.upd_item(user)
            if user is None:
                raise UserNotFoundError(login)

            self.__uow.commit()

            return user

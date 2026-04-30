from __future__ import annotations

from typing import TYPE_CHECKING

from domain.entities import User
from domain.interfaces import UpdateUserMetaUseCaseInterface
from .exceptions import UserNotFoundError

if TYPE_CHECKING:
    from domain.interfaces import UserUnitOfWorkInterface
    from domain.interfaces.user.types import (
        UserLoginType,
        UserMetaUpdNameType,
        UserMetaUpdAvatarPathType,
        UserMetaUpdTimeBlockType
    )


class UpdateUserMeta(UpdateUserMetaUseCaseInterface[User]):
    """Обновление настроек пользователя."""

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
            name: UserMetaUpdNameType,
            avatar_path: UserMetaUpdAvatarPathType,
            time_block: UserMetaUpdTimeBlockType
    ) -> User:
        """
        Обновление настроек пользователя.

        :param login: Логин пользователя.
        :type login: UserLoginType

        :param name: Имя пользователя.
        :type name: UserMetaUpdNameType

        :param avatar_path: Путь к аватарке пользователя.
        :type avatar_path: UserMetaUpdAvatarPathType

        :param time_block: Время блокировки сессии пользователя.
        :type time_block: UserMetaUpdTimeBlockType

        :return: Пользователь.
        :rtype: User

        :raises UserNotFoundError: Если пользователь не найден.
        """
        with self.__uow:
            user = self.__uow.user_repos.get_item(login)
            if user is None:
                raise UserNotFoundError(login)

            # Mypy ругается на разные типы для property и setter
            user.meta.name = name  # type: ignore
            user.meta.avatar_path = avatar_path  # type: ignore
            user.meta.time_block = time_block  # type: ignore

            upd_user: User | None = self.__uow.user_repos.upd_item(user)
            if upd_user is None:
                raise UserNotFoundError(login)

            self.__uow.commit()

            return upd_user

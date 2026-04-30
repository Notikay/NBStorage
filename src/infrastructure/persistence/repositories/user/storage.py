from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from domain.entities import User
from domain.interfaces import UserRepositoryInterface
from infrastructure.persistence.models import UserORM
from .exceptions import UserCreateError, UserDeleteError, UserDeleteAllError

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from domain.interfaces.user.types import UserLoginType


class UserStorage(UserRepositoryInterface[User]):
    """Хранилище пользователей."""

    def __init__(self, session: Session):
        """
        Инициализация хранилища пользователя.

        :param session: Сессия подключения к хранилищу пользователя.
        :type session: Session
        """
        self.__session = session

    @property
    def session(self) -> Session:
        """
        Сессия подключения к хранилищу.

        Только для чтения.

        :rtype: Session
        """
        return self.__session

    def get_item(self, login: UserLoginType) -> User | None:
        """
        Получение пользователя из хранилища.

        :param login: Логин пользователя.
        :type login: UserLoginType

        :return: Пользователь из хранилища.
        :rtype: User | None
        """
        user_orm = self.__session.get(UserORM, login)
        user = user_orm.to_item() if user_orm else None

        return user

    def get_all_items(self) -> list[User]:
        """
        Получение всех пользователей из хранилища.

        :return: Все пользователи из хранилища.
        :rtype: list[User]
        """
        stmt = select(UserORM)

        users_orm = self.__session.execute(stmt).scalars().all()
        users = [user.to_item() for user in users_orm]

        return users

    def set_item(self, item: User) -> User:
        """
        Создание пользователя в хранилище.

        :param item: Пользователь.
        :type item: User

        :return: Пользователь из хранилища.
        :rtype: User

        :raises UserCreateError: Если не удалось создать пользователя.
        """
        user_orm = UserORM(
            login=item.login,
            name=item.meta.name,
            avatar_path=str(item.meta.avatar_path),
            time_block=item.meta.time_block,
            salt=item.meta.salt,
            password=item.password
        )
        self.__session.add(user_orm)

        try:
            self.__session.flush()
        except IntegrityError:
            raise UserCreateError(item.login)

        user = user_orm.to_item()

        return user

    def upd_item(self, item: User) -> User | None:
        """
        Обновление пользователя в хранилище.

        :param item: Обновленный пользователь.
        :type item: User

        :return: Обновленный пользователь из хранилища.
        :rtype: User | None
        """
        stmt = (
            update(UserORM)
            .where(UserORM.login == item.login)
            .values(
                name=item.meta.name,
                avatar_path=str(item.meta.avatar_path),
                time_block=item.meta.time_block,
                password=item.password
            )
            .returning(UserORM)
        )
        user_orm = self.__session.execute(stmt).scalar_one_or_none()
        user = user_orm.to_item() if user_orm else None

        return user

    def del_item(self, login: UserLoginType) -> None:
        """
        Удаление пользователя из хранилища.

        :param login: Логин пользователя.
        :type login: UserLoginType

        :raises UserDeleteError: Если не удалось удалить пользователя.
        """
        stmt = delete(UserORM).where(UserORM.login == login)

        try:
            self.__session.execute(stmt)
            self.__session.flush()
        except IntegrityError:
            raise UserDeleteError(login)

    def del_all_items(self) -> None:
        """
        Удаление всех пользователей из хранилища.

        :raises UserDeleteAllError: Если не удалось удалить всех
                                    пользователей.
        """
        stmt = delete(UserORM)

        try:
            self.__session.execute(stmt)
            self.__session.flush()
        except IntegrityError:
            raise UserDeleteAllError()

from typing import TYPE_CHECKING, Any, cast

from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from domain.entities.user import User
from domain.entities.user.types import UserMetaIDType
from domain.use_cases.user.types import UsersCountType
from infrastructure.database.models.user import UserModel

from .exceptions import (
    DeleteAllUsersError,
    DeleteUserError,
    GetUserError,
    SaveUserError,
)

if TYPE_CHECKING:
    from sqlalchemy.engine import CursorResult


class UserStorage:
    """Хранилище пользователей."""

    def __init__(self, session: Session) -> None:
        self.__session = session

    @property
    def session(self) -> Session:
        """
        Сессия подключения к БД.

        Только для чтения.
        """
        return self.__session

    def get_by_id(self, item_id: UserMetaIDType) -> User | None:
        """
        Получение пользователя из БД.

        :raises GetUserError: Если не удалось получить пользователя из
                              БД.
        """
        try:
            user_model = self.__session.get(UserModel, item_id)
            return user_model.to_item() if user_model else None
        except SQLAlchemyError as e:
            raise GetUserError(item_id) from e

    def save(self, item: User) -> User:
        """
        Создание пользователя в БД.

        :raises SaveUserError: Если не удалось сохранить пользователя
                               в БД.
        """
        try:
            user_model = self.__session.get(UserModel, item.meta.user_id)
            if user_model is None:
                user_model = UserModel(user_id=item.meta.user_id)
                self.__session.add(user_model)

            user_model.name = item.meta.name
            user_model.avatar_key = item.meta.avatar_key
            user_model.time_block = item.meta.time_block
            user_model.salt = item.meta.salt
            user_model.login = item.login
            user_model.password = item.password

            self.__session.flush()
            self.__session.refresh(user_model)
            return user_model.to_item()
        except SQLAlchemyError as e:
            raise SaveUserError(item.meta.user_id) from e

    def del_by_id(self, item_id: UserMetaIDType) -> None:
        """
        Удаление пользователя из БД.

        :raise DeleteUserError: Если не удалось удалить пользователя из
                                БД.
        """
        try:
            # user_model = self.__session.get(UserModel, item_id)
            # if user_model:
            #     self.__session.delete(user_model)
            stmt = delete(UserModel).where(UserModel.user_id == item_id)
            self.__session.execute(stmt)
        except SQLAlchemyError as e:
            raise DeleteUserError(item_id) from e

    def del_all(self) -> UsersCountType:
        """
        Удаление всех пользователей из БД.

        :raise DeleteAllUsersError: Если не удалось удалить всех
                                    пользователей из БД.
        """
        try:
            # users = self.__session.query(UserModel).all()
            # for user in users:
            #     self.__session.delete(user)
            # return len(users)
            stmt = delete(UserModel)
            result = cast('CursorResult[Any]', self.__session.execute(stmt))
            return result.rowcount or 0
        except SQLAlchemyError as e:
            raise DeleteAllUsersError() from e

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from infrastructure.database.models.user import UserModel
from infrastructure.database.query_services.user.projections import (
    UserInfoProjection,
    UsersInfoCollectionProjection,
)

from .exceptions import GetAllUsersError


class UserProvider:
    """Поставщик данных пользователя из БД."""

    def __init__(self, session: Session) -> None:
        self.__session = session

    @property
    def session(self) -> Session:
        """
        Сессия подключения к БД.

        Только для чтения.
        """
        return self.__session

    def get_all_items(self) -> UsersInfoCollectionProjection:
        """
        Получение данных из БД для всех пользователей.

        :raises GetAllUsersError: Если не удалось получить данные всех
                                  пользователей из БД.
        """
        try:
            stmt = select(
                UserModel.user_id,
                UserModel.name,
                UserModel.avatar_key,
                UserModel.login
            )
            user_models = self.__session.execute(stmt).all()
        except SQLAlchemyError as e:
            raise GetAllUsersError() from e

        return UsersInfoCollectionProjection(
            users_info=[
                UserInfoProjection(
                    user_model.user_id,
                    user_model.name,
                    user_model.avatar_key,
                    user_model.login
                )
                for user_model in user_models
            ]
        )

from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, Self

from domain.entities import Card, User
from domain.interfaces import CardUnitOfWorkInterface, UserUnitOfWorkInterface
from .exceptions import SessionNotInitializedError
from ..repositories import CardStorage, UserStorage

if TYPE_CHECKING:
    from sqlalchemy.orm import sessionmaker, Session


class TransactionManager(
    CardUnitOfWorkInterface[Card],
    UserUnitOfWorkInterface[User]
):
    """Менеджер управления транзакцией."""

    def __init__(self, session_factory: sessionmaker[Session]):
        """
        Инициализация менеджера управления транзакцией.

        :param session_factory: Фабрика подключений к хранилищу данных.
        :type session_factory: sessionmaker
        """
        self.__session_factory = session_factory

        self.__session: Session | None = None
        self.__card_repos: CardStorage | None = None
        self.__user_repos: UserStorage | None = None
        self.__is_committed = False

    @property
    def session(self):
        """
        Сессия подключения к хранилищу.

        Только для чтения.

        :rtype: Session
        """
        return self.__session

    @property
    def card_repos(self) -> CardStorage:
        """
        Хранилище карточек пользователя.

        Только для чтения.

        :rtype: CardStorage
        """
        if self.__card_repos is None:
            if self.__session is None:
                raise SessionNotInitializedError("Ошибка инициализации сессии "
                                                 "подключения к хранилищу "
                                                 "карточек пользователя!")
            self.__card_repos = CardStorage(self.__session)
        return self.__card_repos

    @property
    def user_repos(self) -> UserStorage:
        """
        Хранилище пользователей.

        Только для чтения.

        :rtype: UserStorage
        """
        if self.__user_repos is None:
            if self.__session is None:
                raise SessionNotInitializedError("Ошибка инициализации сессии "
                                                 "подключения к хранилищу "
                                                 "пользователей!")
            self.__user_repos = UserStorage(self.__session)
        return self.__user_repos

    def __enter__(self) -> Self:
        self.__session = self.__session_factory()
        self.__is_committed = False
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> None:
        if self.__session is None:
            raise SessionNotInitializedError()

        if exc_type or (not self.__is_committed):
            self.__session.rollback()
        self.__session.close()
        self.__is_committed = False

    def commit(self) -> None:
        """
        Сохранение изменений в хранилище.

        :raises SessionNotInitializedError: Если сессия не была
                                            инициализирована.
        """
        if self.__session is None:
            raise SessionNotInitializedError()
        self.__session.commit()
        self.__is_committed = True

    def rollback(self) -> None:
        """
        Откат изменений (хранилище не изменено).

        :raises SessionNotInitializedError: Если сессия не была
                                            инициализирована.
        """
        if self.__session is None:
            raise SessionNotInitializedError()
        self.__session.rollback()

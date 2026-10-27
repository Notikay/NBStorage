from types import TracebackType
from typing import Self

from sqlalchemy.orm import Session, sessionmaker

from domain.interfaces.card import CardRepository, CardUnitOfWork
from domain.interfaces.user import UserRepository, UserUnitOfWork

from ..repositories.card import CardStorage
from ..repositories.user import UserStorage
from .exceptions import SessionNotInitializedError


class TransactionManager(CardUnitOfWork, UserUnitOfWork):
    """Менеджер управления транзакцией."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.__session_factory = session_factory

        self.__session: Session | None = None
        self.__card_repos: CardStorage | None = None
        self.__user_repos: UserStorage | None = None
        self.__is_committed = False

    @property
    def session(self) -> Session | None:
        """
        Сессия подключения к БД.

        Только для чтения.
        """
        return self.__session

    @property
    def card_repos(self) -> CardRepository:
        """
        Хранилище карточек пользователя.

        Только для чтения.

        :raises SessionNotInitializedError: Если сессия подключения к
                                            БД не была инициализирована.
        """
        if self.__card_repos is None:
            if self.__session is None:
                raise SessionNotInitializedError()
            self.__card_repos = CardStorage(self.__session)
        return self.__card_repos

    @property
    def user_repos(self) -> UserRepository:
        """
        Хранилище пользователей.

        Только для чтения.

        :raises SessionNotInitializedError: Если сессия подключения к
                                            БД не была инициализирована.
        """
        if self.__user_repos is None:
            if self.__session is None:
                raise SessionNotInitializedError()
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
        Сохранение изменений в БД.

        :raises SessionNotInitializedError: Если сессия подключения к
                                            БД не была инициализирована.
        """
        if self.__session is None:
            raise SessionNotInitializedError()
        self.__session.commit()
        self.__is_committed = True

    def rollback(self) -> None:
        """
        Откат изменений (данные в БД не изменены).

        :raises SessionNotInitializedError: Если сессия подключения к
                                            БД не была инициализирована.
        """
        if self.__session is None:
            raise SessionNotInitializedError()
        self.__session.rollback()

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from domain.interfaces.units.card import CardUnitOfWorkInterface
from domain.interfaces.units.user import UserUnitOfWorkInterface
from domain.entities import Card, User
from .exceptions import SessionIsNotInitializedError
from ..repositories import CardStorage, UserStorage

if TYPE_CHECKING:
    from sqlalchemy.orm import sessionmaker, Session

    from domain.interfaces.base.base_types import (
        UOWErrorType,
        UOWValueErrorType,
        UOWTracebackErrorType
    )


class TransactionStateManager(
    CardUnitOfWorkInterface[Card],
    UserUnitOfWorkInterface[User]
):
    """
    Менеджер состояния транзакций.

    :ivar __session_factory: Атрибут фабрики подключений к хранилищу
                             данных.
    :type __session_factory: sessionmaker

    :ivar __session: Атрибут сессии подключения к хранилищу данных.
    :type __session: Session | None

    :ivar __card_repos: Атрибут хранилища карточек пользователей.
    :type __card_repos: CardStorage | None

    :ivar __user_repos: Атрибут хранилища пользователей.
    :type __user_repos: UserStorage | None
    """

    def __init__(self, session_factory: sessionmaker[Session]):
        """
        Инициализация менеджера состояния транзакций.

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
        return self.__session

    @property
    def card_repos(self) -> CardStorage:
        if self.__card_repos is None:
            if self.__session is None:
                raise SessionIsNotInitializedError()
            self.__card_repos = CardStorage(self.__session)
        return self.__card_repos

    @property
    def user_repos(self) -> UserStorage:
        if self.__user_repos is None:
            if self.__session is None:
                raise SessionIsNotInitializedError()
            self.__user_repos = UserStorage(self.__session)
        return self.__user_repos

    def __enter__(self) -> Self:
        self.__session = self.__session_factory()
        self.__is_committed = False
        return self

    def __exit__(
            self,
            exc_type: UOWErrorType,
            exc_val: UOWValueErrorType,
            exc_tb: UOWTracebackErrorType
    ) -> None:
        if self.__session is None:
            raise SessionIsNotInitializedError()

        if exc_type or (not self.__is_committed):
            self.__session.rollback()
        self.__session.close()
        self.__is_committed = False

    def commit(self) -> None:
        """Сохранение изменений в хранилище."""
        if self.__session is None:
            raise SessionIsNotInitializedError()
        self.__session.commit()
        self.__is_committed = True

    def rollback(self) -> None:
        """Откат изменений (хранилище не изменено)."""
        if self.__session is None:
            raise SessionIsNotInitializedError()
        self.__session.rollback()

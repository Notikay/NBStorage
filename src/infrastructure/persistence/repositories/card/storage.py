from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from domain.entities import Card
from domain.interfaces import CardRepositoryInterface
from infrastructure.persistence.models import CardORM
from .exceptions import CardCreateError, CardDeleteError, CardDeleteAllError

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from domain.interfaces.card.types import (
        CardMetaUserLoginType,
        CardMetaCardIDType
    )


class CardStorage(CardRepositoryInterface[Card]):
    """Хранилище карточек пользователей."""

    def __init__(self, session: Session):
        """
        Инициализация хранилища карточек пользователя.

        :param session: Сессия подключения к хранилищу карточек
                        пользователя.
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

    def get_item(
            self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType
    ) -> Card | None:
        """
        Получение карточки пользователя из хранилища.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: CardMetaCardIDType

        :return: Карточка пользователя из хранилища.
        :rtype: Card | None
        """
        card_orm = self.__session.get(CardORM, (user_login, card_id))
        card = card_orm.to_item() if card_orm else None

        return card

    def get_all_items(self, user_login: CardMetaUserLoginType) -> list[Card]:
        """
        Получение всех карточек пользователя из хранилища.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :return: Все карточки пользователя из хранилища.
        :rtype: list[Card]
        """
        stmt = select(CardORM).where(CardORM.user_login == user_login)

        cards_orm = self.__session.execute(stmt).scalars().all()
        cards = [card.to_item() for card in cards_orm]

        return cards

    def set_item(self, item: Card) -> Card:
        """
        Создание карточки пользователя в хранилище.

        :param item: Карточка пользователя.
        :type item: Card

        :return: Карточка пользователя из хранилища.
        :rtype: Card

        :raises CardCreateError: Если не удалось создать карточку
                                 пользователя.
        """
        card_orm = CardORM(
            user_login=item.meta.user_login,
            card_id=item.meta.card_id,
            title=item.meta.title,
            icon_path=str(item.meta.icon_path),
            key=item.meta.key,
            username=item.username,
            email=item.email,
            password=item.password,
            url=item.url,
            description=item.description
        )
        self.__session.add(card_orm)

        try:
            self.__session.flush()
        except IntegrityError:
            raise CardCreateError(item.meta.user_login, item.meta.card_id)

        card = card_orm.to_item()

        return card

    def upd_item(self, item: Card) -> Card | None:
        """
        Обновление карточки пользователя в хранилище.

        :param item: Обновленная карточка пользователя.
        :type item: Card

        :return: Обновленная карточка пользователя из хранилища.
        :rtype: Card | None
        """
        stmt = (
            update(CardORM)
            .where(
                CardORM.user_login == item.meta.user_login,
                CardORM.card_id == item.meta.card_id
            )
            .values(
                title=item.meta.title,
                icon_path=str(item.meta.icon_path),
                username=item.username,
                email=item.email,
                password=item.password,
                url=item.url,
                description=item.description
            )
            .returning(CardORM)
        )
        card_orm = self.__session.execute(stmt).scalar_one_or_none()
        card = card_orm.to_item() if card_orm else None

        return card

    def del_item(self,
            user_login: CardMetaUserLoginType,
            card_id: CardMetaCardIDType
    ) -> None:
        """
        Удаление карточки пользователя из хранилища.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: CardMetaCardIDType

        :raises CardDeleteError: Если не удалось удалить карточку
                                 пользователя.
        """
        stmt = delete(CardORM).where(
            CardORM.user_login == user_login,
            CardORM.card_id == card_id
        )

        try:
            self.__session.execute(stmt)
            self.__session.flush()
        except IntegrityError:
            raise CardDeleteError(user_login, card_id)

    def del_all_items(self, user_login: CardMetaUserLoginType) -> None:
        """
        Удаление всех карточек пользователя из хранилища.

        :param user_login: Логин пользователя.
        :type user_login: CardMetaUserLoginType

        :raises CardDeleteAllError: Если не удалось удалить все
                                    карточки пользователя.
        """
        stmt = delete(CardORM).where(CardORM.user_login == user_login)

        try:
            self.__session.execute(stmt)
            self.__session.flush()
        except IntegrityError:
            raise CardDeleteAllError(user_login)

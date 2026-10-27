from typing import TYPE_CHECKING, Any, cast

import structlog
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from domain.entities.card import Card
from domain.entities.card.types import CardMetaIDType, CardMetaUserIDType
from domain.use_cases.card.types import CardsCountType
from infrastructure.database.models.card import CardModel

from .exceptions import (
    DeleteAllCardsError,
    DeleteCardError,
    GetCardError,
    SaveCardError,
)

if TYPE_CHECKING:
    from sqlalchemy.engine import CursorResult

logger = structlog.get_logger(__name__)


class CardStorage:
    """Хранилище карточек пользователей."""

    def __init__(self, session: Session) -> None:
        self.__session = session

    @property
    def session(self) -> Session:
        """
        Сессия подключения к БД.

        Только для чтения.
        """
        return self.__session

    def get_by_id(self, item_id: CardMetaIDType) -> Card | None:
        """
        Получение карточки пользователя из БД.

        :raises GetCardError: Если не удалось получить карточку
                              пользователя из БД.
        """
        try:
            card_model = self.__session.get(CardModel, item_id)
            return card_model.to_item() if card_model else None
        except SQLAlchemyError as e:
            logger.debug("sql_get_error", card_id=item_id, error=str(e))
            raise GetCardError(item_id) from e

    def save(self, item: Card) -> Card:
        """
        Создание карточки пользователя в БД.

        :raises SaveCardError: Если не удалось сохранить карточку
                               пользователя в БД.
        """
        try:
            card_model = self.__session.get(CardModel, item.meta.card_id)
            if card_model is None:
                card_model = CardModel(
                    card_id=item.meta.card_id,
                    user_id=item.meta.user_id
                )
                self.__session.add(card_model)

            card_model.title = item.meta.title
            card_model.icon_key = item.meta.icon_key
            card_model.key = item.meta.key
            card_model.username = item.username
            card_model.email = item.email
            card_model.password = item.password
            card_model.url = item.url
            card_model.description = item.description

            self.__session.flush()
            self.__session.refresh(card_model)

            return card_model.to_item()
        except SQLAlchemyError as e:
            logger.debug(
                "sql_save_error",
                user_id=item.meta.user_id,
                card_id=item.meta.card_id,
                error=str(e)
            )
            raise SaveCardError(item.meta.card_id) from e

    def del_by_id(self, item_id: CardMetaIDType) -> None:
        """
        Удаление карточки пользователя из БД.

        :raise DeleteCardError: Если не удалось удалить карточку
                                пользователя из БД.
        """
        try:
            stmt = delete(CardModel).where(CardModel.card_id == item_id)
            self.__session.execute(stmt)
        except SQLAlchemyError as e:
            logger.debug("sql_del_error", card_id=item_id, error=str(e))
            raise DeleteCardError(item_id) from e

    def del_all_by_user_id(self, user_id: CardMetaUserIDType) -> CardsCountType:
        """
        Удаление всех карточек пользователя из БД.

        :raise DeleteAllCardsError: Если не удалось удалить все
                                    карточки пользователя из БД.
        """
        try:
            stmt = delete(CardModel).where(CardModel.user_id == user_id)
            result = cast('CursorResult[Any]', self.__session.execute(stmt))
            return result.rowcount or 0
        except SQLAlchemyError as e:
            logger.debug("sql_del_all_error", user_id=user_id, error=str(e))
            raise DeleteAllCardsError(user_id) from e

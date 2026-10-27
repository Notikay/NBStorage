from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from infrastructure.database.models.card import CardModel
from infrastructure.database.models.types import CardModelCardIDType
from infrastructure.database.query_services.card.projections import (
    CardInfoProjection,
    CardsInfoCollectionProjection,
)

from .exceptions import GetAllCardsError


class CardProvider:
    """Поставщик данных карточек пользователя из БД."""

    def __init__(self, session: Session) -> None:
        self.__session = session

    @property
    def session(self) -> Session:
        """
        Сессия подключения к БД.

        Только для чтения.
        """
        return self.__session

    def get_all_items(
            self,
            user_id: CardModelCardIDType
    ) -> CardsInfoCollectionProjection:
        """
        Получение данных из БД для всех карточек пользователя по его ID.

        :raises GetAllCardsError: Если не удалось получить данные всех
                                  карточек пользователя из БД.
        """
        try:
            stmt = (
                select(CardModel.card_id, CardModel.title, CardModel.icon_key)
                .where(CardModel.user_id == user_id)
            )
            card_models = self.__session.execute(stmt).all()
        except SQLAlchemyError as e:
            raise GetAllCardsError() from e

        return CardsInfoCollectionProjection(
            user_id=user_id,
            cards_info=[
                CardInfoProjection(
                    card_model.card_id,
                    card_model.title,
                    card_model.icon_key
                )
                for card_model in card_models
            ]
        )

from domain.interfaces import ResultPresenter
from domain.interfaces.card import CardQueryService
from infrastructure.database.query_services.card.projections import (
    CardsInfoCollectionProjection,
)
from interface_adapters.presenters.views import MapView
from shared.errors import DataBaseError, InternalError

from .schemas import GetCardsInfoSchema


class GetCardsInfo:
    """Получение информации о карточках пользователя."""

    def __init__(
            self,
            query_service: CardQueryService[CardsInfoCollectionProjection],
            presenter: ResultPresenter[CardsInfoCollectionProjection, MapView]
    ) -> None:
        self.__query_service = query_service
        self.__presenter = presenter

    def __call__(self, data: GetCardsInfoSchema) -> MapView:
        try:
            result = self.__query_service.get_all_items(data.user_id)
            return self.__presenter.show_success(result)
        except DataBaseError as e:
            raise DataBaseError(
                "Ошибка чтения информации о карточках пользователя!"
            ) from e
        except Exception as e:
            raise InternalError(
                "Внутренняя ошибка при получении информации о карточках пользователя!"
            ) from e

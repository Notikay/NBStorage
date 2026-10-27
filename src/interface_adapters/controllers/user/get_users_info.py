from domain.interfaces import ResultPresenter
from domain.interfaces.user import UserQueryService
from infrastructure.database.query_services.user.projections import (
    UsersInfoCollectionProjection,
)
from interface_adapters.presenters.views import MapView
from shared.errors import DataBaseError, InternalError


class GetUsersInfo:
    """Получение информации о пользователях."""

    def __init__(
            self,
            query_service: UserQueryService[UsersInfoCollectionProjection],
            presenter: ResultPresenter[UsersInfoCollectionProjection, MapView]
    ) -> None:
        self.__query_service = query_service
        self.__presenter = presenter

    def __call__(self) -> MapView:
        try:
            result = self.__query_service.get_all_items()
            return self.__presenter.show_success(result)
        except DataBaseError as e:
            raise DataBaseError("Ошибка чтения информации о пользователях!") from e
        except Exception as e:
            raise InternalError(
                "Внутренняя ошибка при получении информации о пользователях!"
            ) from e

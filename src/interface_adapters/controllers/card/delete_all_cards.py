from domain.interfaces import CMDUseCase, ResultPresenter
from domain.use_cases.card.commands import DeleteAllCardsCommand
from domain.use_cases.card.types import CardsCountType
from interface_adapters.presenters.views import MapView
from shared.errors import DataBaseError, InternalError, StorageError

from .schemas import DeleteAllCardsSchema


class DeleteAllCards:
    """Удаление всех карточек пользователя."""

    def __init__(
            self,
            use_case: CMDUseCase[DeleteAllCardsCommand, CardsCountType],
            presenter: ResultPresenter[CardsCountType, MapView]
    ) -> None:
        self.__use_case = use_case
        self.__presenter = presenter

    def __call__(self, data: DeleteAllCardsSchema) -> MapView:
        try:
            cmd = DeleteAllCardsCommand(**data.model_dump())
            result = self.__use_case(cmd)
            return self.__presenter.show_success(result)
        except DataBaseError as e:
            raise DataBaseError("Не удалось подключиться к БД!") from e
        except StorageError as e:
            raise StorageError("Не удалось удалить карточки пользователя!") from e
        except Exception as e:
            raise InternalError(
                "Внутренняя ошибка при удалении карточек пользователя"
            ) from e

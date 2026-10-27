from domain.interfaces import CMDUseCase, NonePresenter
from domain.use_cases.card.commands import DeleteCardCommand
from infrastructure.database.repositories.card.exceptions import DeleteCardError
from infrastructure.database.uow.exceptions import SessionNotInitializedError
from interface_adapters.presenters.views import MapView
from shared.errors import DataBaseError, InternalError, StorageError

from .schemas import DeleteCardSchema

ERRORS = (DeleteCardError, SessionNotInitializedError)


class DeleteCard:
    """Удаление карточки пользователя."""

    def __init__(
            self,
            use_case: CMDUseCase[DeleteCardCommand, None],
            presenter: NonePresenter[MapView]
    ) -> None:
        self.__use_case = use_case
        self.__presenter = presenter

    def __call__(self, data: DeleteCardSchema) -> MapView:
        try:
            cmd = DeleteCardCommand(**data.model_dump())
            self.__use_case(cmd)
            return self.__presenter.show_success()
        except DataBaseError as e:
            raise DataBaseError("Не удалось подключиться к БД!") from e
        except StorageError as e:
            raise StorageError("Не удалось удалить карточку пользователя!") from e
        except Exception as e:
            raise InternalError(
                "Внутренняя ошибка при удалении карточки пользователя"
            ) from e

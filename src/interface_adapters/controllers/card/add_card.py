import structlog

from domain.entities.card import Card
from domain.interfaces import CMDUseCase, ResultPresenter
from domain.use_cases.card.commands import CreateCardCommand
from interface_adapters.presenters.views import MapView
from shared.errors import DataBaseError, InternalError, StorageError, ValidationError

from .schemas import AddCardSchema

logger = structlog.get_logger(__name__)


class AddCard:
    """Добавление карточки пользователя."""

    def __init__(
            self,
            use_case: CMDUseCase[CreateCardCommand, Card],
            presenter: ResultPresenter[Card, MapView]
    ) -> None:
        self.__use_case = use_case
        self.__presenter = presenter

    def __call__(self, data: AddCardSchema) -> MapView:
        try:
            cmd = CreateCardCommand(**data.model_dump())
            result = self.__use_case(cmd)
            return self.__presenter.show_success(result)
        except DataBaseError as e:
            logger.debug(e.log_event, error=str(e), code=e.code)
            raise DataBaseError("Не удалось подключиться к БД!") from e
        except ValidationError as e:
            logger.debug(e.log_event, error=str(e), code=e.code)
            raise ValidationError(
                "Некорректные данные (метаданные) карточки пользователя!"
            ) from e
        except StorageError as e:
            logger.debug(e.log_event, error=str(e), code=e.code)
            raise StorageError("Не удалось сохранить карточку пользователя!") from e
        except Exception as e:
            logger.debug("py_exception", error=str(e))
            raise InternalError(
                "Внутренняя ошибка при добавлении карточки пользователя"
            ) from e

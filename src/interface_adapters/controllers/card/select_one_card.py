from domain.entities.card import Card
from domain.interfaces import CMDUseCase, ResultPresenter
from domain.use_cases.card.commands import ChooseCardCommand
from interface_adapters.presenters.views import MapView
from shared.errors import (
    DataBaseError,
    InternalError,
    NotFoundError,
    StorageError,
    ValidationError,
)

from .schemas import SelectOneCardSchema


class SelectOneCard:
    """Выбор одной карточки пользователя."""

    def __init__(
            self,
            use_case: CMDUseCase[ChooseCardCommand, Card],
            presenter: ResultPresenter[Card, MapView]
    ) -> None:
        self.__use_case = use_case
        self.__presenter = presenter

    def __call__(self, data: SelectOneCardSchema) -> MapView:
        try:
            cmd = ChooseCardCommand(**data.model_dump())
            result = self.__use_case(cmd)
            return self.__presenter.show_success(result)
        except DataBaseError as e:
            raise DataBaseError("Не удалось подключиться к БД!") from e
        except StorageError as e:
            raise StorageError("Не удалось получить карточку пользователя!") from e
        except NotFoundError as e:
            raise NotFoundError("Карточка пользователя не найдена!") from e
        except ValidationError as e:
            raise ValidationError(
                "Некорректные данные (метаданные) карточки пользователя!"
            ) from e
        except Exception as e:
            raise InternalError(
                "Внутренняя ошибка при выборе карточки пользователя"
            ) from e

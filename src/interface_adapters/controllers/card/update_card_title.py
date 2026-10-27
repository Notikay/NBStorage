from domain.entities.card import Card
from domain.interfaces import CMDUseCase, ResultPresenter
from domain.use_cases.card.commands import UpdateCardMetaCommand
from interface_adapters.presenters.views import MapView
from shared.errors import (
    DataBaseError,
    InternalError,
    NotFoundError,
    StorageError,
    ValidationError,
)

from .schemas import UpdateCardTitleSchema


class UpdateCardTitle:
    """Обновление названия карточки пользователя."""

    def __init__(
            self,
            use_case: CMDUseCase[UpdateCardMetaCommand, Card],
            presenter: ResultPresenter[Card, MapView]
    ) -> None:
        self.__use_case = use_case
        self.__presenter = presenter

    def __call__(self, data: UpdateCardTitleSchema) -> MapView:
        try:
            cmd = UpdateCardMetaCommand(**data.model_dump())
            result = self.__use_case(cmd)
            return self.__presenter.show_success(result)
        except DataBaseError as e:
            raise DataBaseError("Не удалось подключиться к БД!") from e
        except StorageError as e:
            raise StorageError(
                "Не удалось получить/сохранить карточку пользователя!"
            ) from e
        except NotFoundError as e:
            raise NotFoundError("Карточка пользователя не найдена!") from e
        except ValidationError as e:
            raise ValidationError("Некорректное название карточки пользователя!") from e
        except Exception as e:
            raise InternalError(
                "Внутренняя ошибка при обновлении названия карточки пользователя"
            ) from e

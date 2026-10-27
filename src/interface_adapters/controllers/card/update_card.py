from domain.entities.card import Card
from domain.interfaces import CMDUseCase, ResultPresenter
from domain.use_cases.card.commands import UpdateCardCommand
from interface_adapters.presenters.views import MapView
from shared.errors import (
    DataBaseError,
    InternalError,
    NotFoundError,
    StorageError,
    ValidationError,
)

from .schemas import UpdateCardSchema


class UpdateCard:
    """Обновление карточки пользователя."""

    def __init__(
            self,
            use_case: CMDUseCase[UpdateCardCommand, Card],
            presenter: ResultPresenter[Card, MapView]
    ) -> None:
        self.__use_case = use_case
        self.__presenter = presenter

    def __call__(self, data: UpdateCardSchema) -> MapView:
        try:
            cmd = UpdateCardCommand(**data.model_dump())
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
            raise ValidationError(
                "Некорректные данные (метаданные) карточки пользователя!"
            ) from e
        except Exception as e:
            raise InternalError(
                "Внутренняя ошибка при обновлении карточки пользователя"
            ) from e

from domain.entities.user import User
from domain.interfaces import CMDUseCase, ResultPresenter
from domain.use_cases.user.commands import UpdateUserCommand
from interface_adapters.presenters.views import MapView
from shared.errors import (
    DataBaseError,
    InternalError,
    NotFoundError,
    StorageError,
    ValidationError,
)

from .schemas import UpdateUserSchema


class UpdateUser:
    """Обновление пользователя."""

    def __init__(
            self,
            use_case: CMDUseCase[UpdateUserCommand, User],
            presenter: ResultPresenter[User, MapView]
    ) -> None:
        self.__use_case = use_case
        self.__presenter = presenter

    def __call__(self, data: UpdateUserSchema) -> MapView:
        try:
            cmd = UpdateUserCommand(**data.model_dump())
            result = self.__use_case(cmd)
            return self.__presenter.show_success(result)
        except DataBaseError as e:
            raise DataBaseError("Не удалось подключиться к БД!") from e
        except StorageError as e:
            raise StorageError("Не удалось получить/сохранить пользователя!") from e
        except NotFoundError as e:
            raise NotFoundError("Пользователь не найден!") from e
        except ValidationError as e:
            raise ValidationError(
                "Некорректные данные (метаданные) пользователя!"
            ) from e
        except Exception as e:
            raise InternalError("Внутренняя ошибка при обновлении пользователя") from e

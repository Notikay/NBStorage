from domain.entities.user import User
from domain.interfaces import CMDUseCase, ResultPresenter
from domain.use_cases.user.commands import UpdateUserMetaCommand
from interface_adapters.presenters.views import MapView
from shared.errors import (
    DataBaseError,
    InternalError,
    NotFoundError,
    StorageError,
    ValidationError,
)

from .schemas import UpdateUserSettingsSchema


class UpdateUserSettings:
    """Обновление настроек пользователя."""

    def __init__(
            self,
            use_case: CMDUseCase[UpdateUserMetaCommand, User],
            presenter: ResultPresenter[User, MapView]
    ) -> None:
        self.__use_case = use_case
        self.__presenter = presenter

    def __call__(self, data: UpdateUserSettingsSchema) -> MapView:
        try:
            cmd = UpdateUserMetaCommand(**data.model_dump())
            result = self.__use_case(cmd)
            return self.__presenter.show_success(result)
        except DataBaseError as e:
            raise DataBaseError("Не удалось подключиться к БД!") from e
        except StorageError as e:
            raise StorageError("Не удалось получить/сохранить пользователя!") from e
        except NotFoundError as e:
            raise NotFoundError("Пользователь не найден!") from e
        except ValidationError as e:
            raise ValidationError("Некорректные настройки пользователя!") from e
        except Exception as e:
            raise InternalError(
                "Внутренняя ошибка при обновлении настроек пользователя"
            ) from e

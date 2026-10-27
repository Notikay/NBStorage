from domain.interfaces import CMDUseCase, NonePresenter
from domain.use_cases.user.commands import DeleteUserCommand
from interface_adapters.presenters.views import MapView
from shared.errors import DataBaseError, InternalError, StorageError

from .schemas import DeleteUserSchema


class DeleteUser:
    """Удаление пользователя."""

    def __init__(
            self,
            use_case: CMDUseCase[DeleteUserCommand, None],
            presenter: NonePresenter[MapView]
    ) -> None:
        self.__use_case = use_case
        self.__presenter = presenter

    def __call__(self, data: DeleteUserSchema) -> MapView:
        try:
            cmd = DeleteUserCommand(**data.model_dump())
            self.__use_case(cmd)
            return self.__presenter.show_success()
        except DataBaseError as e:
            raise DataBaseError("Не удалось подключиться к БД!") from e
        except StorageError as e:
            raise StorageError("Не удалось удалить пользователя!") from e
        except Exception as e:
            raise InternalError("Внутренняя ошибка при удалении пользователя") from e

from domain.interfaces import NoneUseCase, ResultPresenter
from domain.use_cases.user.types import UsersCountType
from interface_adapters.presenters.views import MapView
from shared.errors import DataBaseError, InternalError, StorageError


class DeleteAllUsers:
    """Удаление всех пользователей."""

    def __init__(
            self,
            use_case: NoneUseCase[UsersCountType],
            presenter: ResultPresenter[UsersCountType, MapView]
    ) -> None:
        self.__use_case = use_case
        self.__presenter = presenter

    def __call__(self) -> MapView:
        try:
            result = self.__use_case()
            return self.__presenter.show_success(result)
        except DataBaseError as e:
            raise DataBaseError("Не удалось подключиться к БД!") from e
        except StorageError as e:
            raise StorageError("Не удалось удалить пользователей!") from e
        except Exception as e:
            raise InternalError("Внутренняя ошибка при удалении пользователей") from e

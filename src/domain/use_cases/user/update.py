import structlog

from domain.entities.user import User
from domain.interfaces.user import UserUnitOfWork

from .commands import UpdateUserCommand
from .exceptions import UserNotFoundError

logger = structlog.getLogger(__name__)


class UpdateUser:
    """Обновление пользователя."""

    def __init__(self, uow: UserUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self, cmd: UpdateUserCommand) -> User:
        """
        Получение пользователя, обновление параметров и сохранение в
        хранилище.

        :raises UserNotFoundError: Если пользователь не найден.
        """
        with self.__uow:
            user = self.__uow.user_repos.get_by_id(cmd.user_id)
            if user is None:
                raise UserNotFoundError(cmd.user_id)

            user.login = cmd.login
            user.password = cmd.password

            user.hash_password()

            upd_user = self.__uow.user_repos.save(user)

            self.__uow.commit()

            logger.info("user_updated", user_id=upd_user.meta.user_id)

            return upd_user

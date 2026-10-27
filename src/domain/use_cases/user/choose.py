import structlog

from domain.entities.user import User
from domain.interfaces.user import UserUnitOfWork

from .commands import ChooseUserCommand
from .exceptions import UserNotFoundError

logger = structlog.getLogger(__name__)


class ChooseUser:
    """Получение пользователя."""

    def __init__(self, uow: UserUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self, cmd: ChooseUserCommand) -> User:
        """
        Получение пользователя из хранилища.

        :raises UserNotFoundError: Если пользователь не найден.
        """
        with self.__uow:
            user: User | None = self.__uow.user_repos.get_by_id(cmd.user_id)
            if user is None:
                raise UserNotFoundError(cmd.user_id)

            logger.info("user_chosen", user_id=user.meta.user_id)

            return user

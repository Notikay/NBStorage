import structlog

from domain.interfaces.user import UserUnitOfWork

from .commands import DeleteUserCommand

logger = structlog.getLogger(__name__)


class DeleteUser:
    """Удаление пользователя."""

    def __init__(self, uow: UserUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self, cmd: DeleteUserCommand) -> None:
        """Удаление из хранилища по ID пользователя."""
        with self.__uow:
            self.__uow.user_repos.del_by_id(cmd.user_id)

            self.__uow.commit()

            logger.info("user_deleted", user_id=cmd.user_id)

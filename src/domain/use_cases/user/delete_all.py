import structlog

from domain.interfaces.user import UserUnitOfWork

from .types import UsersCountType

logger = structlog.getLogger(__name__)


class DeleteAllUsers:
    """Удаление всех пользователей."""

    def __init__(self, uow: UserUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self) -> UsersCountType:
        """Удаление из хранилища пользователей."""
        with self.__uow:
            users_count = self.__uow.user_repos.del_all()

            self.__uow.commit()

            logger.info("all_users_deleted", users_count=users_count)

            return users_count

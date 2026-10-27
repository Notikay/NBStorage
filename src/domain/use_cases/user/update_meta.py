import structlog

from domain.entities.user import User
from domain.interfaces.user import UserUnitOfWork

from .commands import UpdateUserMetaCommand
from .exceptions import UserNotFoundError

logger = structlog.getLogger(__name__)


class UpdateUserMeta:
    """Обновление метаданных пользователя."""

    def __init__(self, uow: UserUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self, cmd: UpdateUserMetaCommand) -> User:
        """
        Получение карточки пользователя, обновление метаданных и
        сохранение в хранилище.

        :raises UserNotFoundError: Если пользователь не найден.
        """
        with self.__uow:
            user: User | None = self.__uow.user_repos.get_by_id(cmd.user_id)
            if user is None:
                raise UserNotFoundError(cmd.user_id)

            user.meta.name = cmd.name
            user.meta.time_block = cmd.time_block

            upd_user = self.__uow.user_repos.save(user)

            self.__uow.commit()

            logger.info("user_meta_updated", user_id=upd_user.meta.user_id)

            return upd_user

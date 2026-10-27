import structlog

from domain.entities.user import User, UserMeta
from domain.interfaces.user import UserUnitOfWork

from .commands import CreateUserCommand

logger = structlog.getLogger(__name__)


class CreateUser:
    """Создание пользователя."""

    def __init__(self, uow: UserUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self, cmd: CreateUserCommand) -> User:
        """Формирование пользователя и сохранение в хранилище."""
        with self.__uow:
            user = User(
                UserMeta(cmd.name, None, cmd.time_block),
                cmd.login,
                cmd.password
            )
            user.hash_password()

            user = self.__uow.user_repos.save(user)

            self.__uow.commit()

            logger.info("user_created", user_id=user.meta.user_id)

            return user

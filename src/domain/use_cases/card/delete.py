import structlog

from domain.interfaces.card import CardUnitOfWork

from .commands import DeleteCardCommand

logger = structlog.getLogger(__name__)


class DeleteCard:
    """Удаление карточки пользователя."""

    def __init__(self, uow: CardUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self, cmd: DeleteCardCommand) -> None:
        """Удаление из хранилища по ID карточки пользователя."""
        with self.__uow:
            self.__uow.card_repos.del_by_id(cmd.card_id)

            self.__uow.commit()

            logger.info("card_deleted", card_id=cmd.card_id)

import structlog

from domain.interfaces.card import CardUnitOfWork

from .commands import DeleteAllCardsCommand
from .types import CardsCountType

logger = structlog.getLogger(__name__)


class DeleteAllCards:
    """Удаление всех карточек пользователя."""

    def __init__(self, uow: CardUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self, cmd: DeleteAllCardsCommand) -> CardsCountType:
        """Удаление из хранилища по ID пользователя."""
        with self.__uow:
            cards_count = self.__uow.card_repos.del_all_by_user_id(cmd.user_id)

            self.__uow.commit()

            logger.info(
                "all_cards_deleted",
                user_id=cmd.user_id,
                cards_count=cards_count
            )

            return cards_count

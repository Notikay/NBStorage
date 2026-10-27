import structlog

from domain.entities.card import Card
from domain.interfaces.card import CardUnitOfWork

from .commands import ChooseCardCommand
from .exceptions import CardNotFoundError

logger = structlog.getLogger(__name__)


class ChooseCard:
    """Получение карточки пользователя."""

    def __init__(self, uow: CardUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self, cmd: ChooseCardCommand) -> Card:
        """
        Получение карточки пользователя из хранилища и ее расшифровка.

        :raises CardNotFoundError: Если карточка пользователя не
                                   найдена.
        """
        with self.__uow:
            card: Card | None = self.__uow.card_repos.get_by_id(cmd.card_id)
            if card is None:
                raise CardNotFoundError(cmd.card_id)
            card.decrypt()

            logger.info(
                "card_chosen",
                user_id=card.meta.user_id,
                card_id=card.meta.card_id
            )

            return card

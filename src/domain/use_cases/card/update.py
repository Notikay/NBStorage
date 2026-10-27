import structlog

from domain.entities.card import Card
from domain.interfaces.card import CardUnitOfWork

from .commands import UpdateCardCommand
from .exceptions import CardNotFoundError

logger = structlog.getLogger(__name__)


class UpdateCard:
    """Обновление карточки пользователя."""

    def __init__(self, uow: CardUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self, cmd: UpdateCardCommand) -> Card:
        """
        Получение карточки пользователя, расшифровка, обновление
        параметров, шифровка и сохранение в хранилище.

        :raises CardNotFoundError: Если карточка пользователя не
                                   найдена.
        """
        with self.__uow:
            card: Card | None = self.__uow.card_repos.get_by_id(cmd.card_id)
            if card is None:
                raise CardNotFoundError(cmd.card_id)
            card.decrypt()

            card.username = cmd.username
            card.email = cmd.email
            card.password = cmd.password
            card.url = cmd.url
            card.description = cmd.description
            card.encrypt()

            upd_card = self.__uow.card_repos.save(card)
            upd_card.decrypt()

            self.__uow.commit()

            logger.info(
                "card_updated",
                user_id=upd_card.meta.user_id,
                card_id=upd_card.meta.card_id
            )

            return upd_card

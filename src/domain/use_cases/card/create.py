import structlog

from domain.entities.card import Card, CardMeta
from domain.interfaces.card import CardUnitOfWork

from .commands import CreateCardCommand

logger = structlog.getLogger(__name__)


class CreateCard:
    """Создание карточки пользователя."""

    def __init__(self, uow: CardUnitOfWork) -> None:
        self.__uow = uow

    def __call__(self, cmd: CreateCardCommand) -> Card:
        """
        Формирование карточки пользователя, шифровка и сохранение в
        хранилище.
        """
        with self.__uow:
            card = Card(
                CardMeta(cmd.title, None, cmd.user_id),
                cmd.username,
                cmd.email,
                cmd.password,
                cmd.url,
                cmd.description
            )
            card.encrypt()

            card = self.__uow.card_repos.save(card)
            card.decrypt()

            self.__uow.commit()

            logger.info(
                "card_created",
                user_id=card.meta.user_id,
                card_id=card.meta.card_id
            )

            return card

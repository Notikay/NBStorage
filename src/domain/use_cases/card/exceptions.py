from domain.entities.card.types import CardMetaIDType
from shared.errors import NotFoundError


class CardNotFoundError(NotFoundError):
    def __init__(self, card_id: CardMetaIDType) -> None:
        self.__card_id = card_id
        super().__init__(f"Карточка пользователя не найдена! -> {card_id=}")

    @property
    def card_id(self) -> CardMetaIDType:
        return self.__card_id

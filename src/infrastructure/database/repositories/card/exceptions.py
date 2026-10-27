from domain.entities.card.types import CardMetaIDType, CardMetaUserIDType
from shared.errors import MessageType, StorageError


class CardStorageError(StorageError):
    def __init__(self, message: MessageType, card_id: CardMetaIDType) -> None:
        super().__init__(message)
        self.__card_id = card_id

    @property
    def card_id(self) -> CardMetaIDType:
        return self.__card_id


class GetCardError(CardStorageError):
    def __init__(self, card_id: CardMetaIDType) -> None:
        super().__init__(
            f"Не удалось получить карточку пользователя! -> {card_id=}",
            card_id
        )


class SaveCardError(CardStorageError):
    def __init__(self, card_id: CardMetaIDType) -> None:
        super().__init__(
            f"Не удалось сохранить карточку пользователя! -> {card_id=}",
            card_id
        )


class DeleteCardError(CardStorageError):
    def __init__(self, card_id: CardMetaIDType) -> None:
        super().__init__(
            f"Не удалось удалить карточку пользователя! -> {card_id=}",
            card_id
        )


class DeleteAllCardsError(StorageError):
    def __init__(self, user_id: CardMetaUserIDType) -> None:
        super().__init__(f"Не удалось удалить все карточки пользователя! -> {user_id=}")
        self.__user_id = user_id

    @property
    def user_id(self) -> CardMetaUserIDType:
        return self.__user_id

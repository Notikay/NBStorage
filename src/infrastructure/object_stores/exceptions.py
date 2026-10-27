from domain.entities.card.types import CardMetaIconKeyType
from shared.errors import MessageType, StoreError


class PortError(StoreError):
    def __init__(self, message: MessageType, key: CardMetaIconKeyType) -> None:
        super().__init__(message)
        self.__key = key

    @property
    def key(self) -> CardMetaIconKeyType:
        return self.__key


class SaveFileError(PortError):
    def __init__(self, key: CardMetaIconKeyType) -> None:
        super().__init__(f"Не удалось сохранить файл! -> {key=}", key)


class DeleteFileError(PortError):
    def __init__(self, key: CardMetaIconKeyType) -> None:
        super().__init__(f"Не удалось удалить файл! -> {key=}", key)

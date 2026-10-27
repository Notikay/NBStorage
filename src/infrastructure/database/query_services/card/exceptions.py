from shared.errors import DataBaseError


class GetAllCardsError(DataBaseError):
    def __init__(self) -> None:
        super().__init__("Не удалось получить данные всех карточек пользователя!")

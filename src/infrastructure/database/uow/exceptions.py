from shared.errors import DataBaseError


class SessionNotInitializedError(DataBaseError):
    def __init__(self) -> None:
        super().__init__("Сессия подключения к БД не была инициализирована!")

from shared.errors import DataBaseError


class GetAllUsersError(DataBaseError):
    def __init__(self) -> None:
        super().__init__("Не удалось получить данные всех пользователей!")

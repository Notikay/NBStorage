from shared.errors import DataBaseError, StoreError


class StoreConnectionError(StoreError):
    def __init__(self) -> None:
        super().__init__("Нет доступа к объектному хранилищу при проверки статуса!")


class DBConnectionError(DataBaseError):
    def __init__(self) -> None:
        super().__init__("Нет доступа к БД при проверки статуса!")

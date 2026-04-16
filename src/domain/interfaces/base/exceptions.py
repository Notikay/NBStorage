from typing import override


class BaseError(Exception):
    """Базовый класс ошибок."""

    @property
    def message(self) -> str:
        return "Произошла внутренняя ошибка!"


class UnitOfWorkError(BaseError):
    """Ошибка транзакции пользователя."""

    @override
    @property
    def message(self) -> str:
        return "Ошибка при управлении состоянием транзакции пользователя!"

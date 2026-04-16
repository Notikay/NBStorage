from typing import override

from domain.interfaces.base.exceptions import BaseError


class UserEntityError(BaseError):
    """Ошибка сущности пользователя."""

    @override
    @property
    def message(self) -> str:
        return "Ошибка сущности пользователя!"


class UserRepositoryError(BaseError):
    """Ошибка репозитория пользователя."""

    @override
    @property
    def message(self) -> str:
        return "Ошибка репозитория пользователя!"


class UserUseCaseError(BaseError):
    """Ошибка бизнес-логики пользователя."""

    @override
    @property
    def message(self) -> str:
        return "Ошибка бизнес-логики пользователя!"

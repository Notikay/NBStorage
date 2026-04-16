from typing import override

from domain.interfaces.base.exceptions import BaseError


class CardEntityError(BaseError):
    """Ошибка сущности карточки пользователя."""

    @override
    @property
    def message(self) -> str:
        return "Ошибка сущности карточки пользователя!"


class CardRepositoryError(BaseError):
    """Ошибка репозитория карточки пользователя."""

    @override
    @property
    def message(self) -> str:
        return "Ошибка репозитория карточки пользователя!"


class CardUseCaseError(BaseError):
    """Ошибка бизнес-логики карточки пользователя."""

    @override
    @property
    def message(self) -> str:
        return "Ошибка бизнес-логики карточки пользователя!"

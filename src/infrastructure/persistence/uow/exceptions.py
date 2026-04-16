from typing import override

from domain.interfaces.base.exceptions import UnitOfWorkError


class SessionIsNotInitializedError(UnitOfWorkError):
    """Ошибка инициализации сессии подключения к хранилищу."""

    @override
    @property
    def message(self) -> str:
        return "Ошибка инициализации сессии подключения к хранилищу!"

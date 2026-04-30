from abc import ABC

from base import AbstractError


class UserInvalidErrorInterface(AbstractError, ABC):
    """Интерфейс ошибки некорректности данных пользователя."""
    ...

class UserNotFoundErrorInterface(AbstractError, ABC):
    """Интерфейс ошибки не найденного пользователя."""
    ...

class CreateUserErrorInterface(AbstractError, ABC):
    """Интерфейс ошибки создания пользователя."""
    ...

class DeleteUserErrorInterface(AbstractError, ABC):
    """Интерфейс ошибки удаления пользователя."""
    ...

class UserSessionNotInitializedErrorInterface(AbstractError, ABC):
    """
    Интерфейс ошибки не инициализированной сессии к хранилищу
    пользователей.
    """
    ...

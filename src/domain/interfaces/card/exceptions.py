from abc import ABC

from base import AbstractError


class CardInvalidErrorInterface(AbstractError, ABC):
    """Интерфейс ошибки некорректности данных карточки пользователя."""
    ...

class CardNotFoundErrorInterface(AbstractError, ABC):
    """Интерфейс ошибки не найденной карточки пользователя."""
    ...

class CreateCardErrorInterface(AbstractError, ABC):
    """Интерфейс ошибки создания карточки пользователя."""
    ...

class DeleteCardErrorInterface(AbstractError, ABC):
    """Интерфейс ошибки удаления карточки пользователя."""
    ...

class CardSessionNotInitializedErrorInterface(AbstractError, ABC):
    """
    Интерфейс ошибки не инициализированной сессии к хранилищу
    карточек пользователя.
    """
    ...

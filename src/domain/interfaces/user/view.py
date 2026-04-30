from abc import ABC
from dataclasses import dataclass

from base import AbstractView


@dataclass
class UserViewInterface(AbstractView, ABC):
    """Интерфейс формата ответа пользователя."""
    ...

from abc import ABC
from dataclasses import dataclass

from base import AbstractView


@dataclass
class CardViewInterface(AbstractView, ABC):
    """Интерфейс формата ответа карточки пользователя."""
    ...

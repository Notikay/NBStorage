from typing import Protocol
from uuid import UUID

from domain.entities.card import Card
from domain.interfaces import Repository


class CardRepository(Repository[Card], Protocol):
    def del_all_by_user_id(self, user_id: UUID) -> int: ...

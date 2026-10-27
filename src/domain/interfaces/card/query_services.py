from typing import Protocol
from uuid import UUID


class CardQueryService[ProjectionT](Protocol):
    def get_all_items(self, user_id: UUID) -> ProjectionT: ...

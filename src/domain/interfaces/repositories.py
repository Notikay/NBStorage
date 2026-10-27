from typing import Protocol
from uuid import UUID

type IDType = UUID


class Repository[EntityT](Protocol):
    def get_by_id(self, item_id: IDType) -> EntityT | None: ...

    def save(self, item: EntityT) -> EntityT: ...

    def del_by_id(self, item_id: IDType) -> None: ...

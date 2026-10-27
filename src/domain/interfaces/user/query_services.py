from typing import Protocol


class UserQueryService[ProjectionT](Protocol):
    def get_all_items(self) -> ProjectionT: ...

from typing import Protocol

from domain.entities.user import User

from ..repositories import Repository


class UserRepository(Repository[User], Protocol):
    def del_all(self) -> int: ...

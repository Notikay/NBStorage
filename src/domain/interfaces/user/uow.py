from typing import Protocol

from ..units_of_work import UnitOfWork
from .repositories import UserRepository


class UserUnitOfWork(UnitOfWork, Protocol):
    @property
    def user_repos(self) -> UserRepository: ...

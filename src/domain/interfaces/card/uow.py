from typing import Protocol

from domain.interfaces import UnitOfWork

from .repositories import CardRepository


class CardUnitOfWork(UnitOfWork, Protocol):
    @property
    def card_repos(self) -> CardRepository: ...

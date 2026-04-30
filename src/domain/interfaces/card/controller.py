from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from base import AbstractController
from .schemas import (
    ChooseCardSchemaInterface,
    ChooseAllCardsSchemaInterface,
    CreateCardSchemaInterface,
    DeleteCardSchemaInterface,
    DeleteAllCardsSchemaInterface,
    UpdateCardSchemaInterface,
    UpdateCardMetaSchemaInterface
)
from .view import CardViewInterface

if TYPE_CHECKING:
    from .schemas import BaseCardSchemaInterface


class BaseCardControllerInterface[T: BaseCardSchemaInterface](
    AbstractController[T, CardViewInterface],
    ABC
):
    """Базовый интерфейс контроллера карточки пользователя."""
    ...


class ChooseCardControllerInterface(
    BaseCardControllerInterface[ChooseCardSchemaInterface],
    ABC
):
    """Интерфейс контроллера получения карточки пользователя."""
    ...


class ChooseAllCardsControllerInterface(
    BaseCardControllerInterface[ChooseAllCardsSchemaInterface],
    ABC
):
    """Интерфейс контроллера получения всех карточек пользователя."""
    ...


class CreateCardControllerInterface(
    BaseCardControllerInterface[CreateCardSchemaInterface],
    ABC
):
    """Интерфейс контроллера создания карточки пользователя."""
    ...


class DeleteCardControllerInterface(
    BaseCardControllerInterface[DeleteCardSchemaInterface],
    ABC
):
    """Интерфейс контроллера удаления карточки пользователя."""
    ...


class DeleteAllCardsControllerInterface(
    BaseCardControllerInterface[DeleteAllCardsSchemaInterface],
    ABC
):
    """Интерфейс контроллера удаления всех карточек пользователя."""
    ...


class UpdateCardControllerInterface(
    BaseCardControllerInterface[UpdateCardSchemaInterface],
    ABC
):
    """Интерфейс контроллера обновления карточки пользователя."""
    ...


class UpdateCardMetaControllerInterface(
    BaseCardControllerInterface[UpdateCardMetaSchemaInterface],
    ABC
):
    """
    Интерфейс контроллера обновления метаданных карточки пользователя.
    """
    ...

from dataclasses import dataclass

from domain.entities.card.types import (
    CardMetaIDType,
    CardMetaTitleType,
    CardMetaUpdTitleType,
    CardMetaUserIDType,
    CardParamType,
    CardUpdParamType,
)


@dataclass(frozen=True, slots=True)
class ChooseCardCommand:
    card_id: CardMetaIDType


@dataclass(frozen=True, slots=True)
class CreateCardCommand:
    user_id: CardMetaUserIDType
    title: CardMetaTitleType
    username: CardParamType
    email: CardParamType
    password: CardParamType
    url: CardParamType
    description: CardParamType


@dataclass(frozen=True, slots=True)
class DeleteCardCommand:
    card_id: CardMetaIDType


@dataclass(frozen=True, slots=True)
class DeleteAllCardsCommand:
    user_id: CardMetaUserIDType


@dataclass(frozen=True, slots=True)
class UpdateCardCommand:
    card_id: CardMetaIDType
    username: CardUpdParamType = None
    email: CardUpdParamType = None
    password: CardUpdParamType = None
    url: CardUpdParamType = None
    description: CardUpdParamType = None


@dataclass(frozen=True, slots=True)
class UpdateCardMetaCommand:
    card_id: CardMetaIDType
    title: CardMetaUpdTitleType = None

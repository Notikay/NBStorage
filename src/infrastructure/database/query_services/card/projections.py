from dataclasses import dataclass

from infrastructure.database.models.types import (
    CardModelCardIDType,
    CardModelIconKeyType,
    CardModelTitleType,
    UserModelIDType,
)


@dataclass(frozen=True, slots=True)
class CardInfoProjection:
    card_id: CardModelCardIDType
    title: CardModelTitleType
    icon_key: CardModelIconKeyType


@dataclass(frozen=True, slots=True)
class CardsInfoCollectionProjection:
    user_id: UserModelIDType
    cards_info: list[CardInfoProjection]

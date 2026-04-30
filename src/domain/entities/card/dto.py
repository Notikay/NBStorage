from typing import TypedDict

type CardDictParamType = str | None


class CardMetaDTO(TypedDict):
    title: str
    icon_path: str
    user_login: str
    card_id: str


class CardDTO(TypedDict):
    meta: CardMetaDTO
    username: CardDictParamType
    email: CardDictParamType
    password: CardDictParamType
    url: CardDictParamType
    description: CardDictParamType

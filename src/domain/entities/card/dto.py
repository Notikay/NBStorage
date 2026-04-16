from typing import TypedDict

type CardDictParamType = str | None


class MetaDataDTO(TypedDict):
    title: str
    icon_path: str
    user_login: str
    card_id: str


class CardDTO(TypedDict):
    metadata: MetaDataDTO
    username: CardDictParamType
    email: CardDictParamType
    password: CardDictParamType
    url: CardDictParamType
    description: CardDictParamType

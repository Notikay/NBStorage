from pydantic import Field

from interface_adapters.controllers.card.schemas import (
    DESCRIPTION_FIELD_ARGS,
    EMAIL_FIELD_ARGS,
    PASSWORD_FIELD_ARGS,
    TITLE_FIELD_ARGS,
    URL_FIELD_ARGS,
    USERNAME_FIELD_ARGS,
)
from interface_adapters.controllers.card.types import (
    CardSchemaDescriptionType,
    CardSchemaEmailType,
    CardSchemaPasswordType,
    CardSchemaTitleType,
    CardSchemaUrlType,
    CardSchemaUsernameType,
)

from .base import BaseSchema


class AddCardRequestSchema(BaseSchema):
    title: CardSchemaTitleType = Field(**TITLE_FIELD_ARGS)  # type: ignore[misc]
    username: CardSchemaUsernameType = Field(**USERNAME_FIELD_ARGS)  # type: ignore[misc]
    email: CardSchemaEmailType = Field(**EMAIL_FIELD_ARGS)  # type: ignore[misc]
    password: CardSchemaPasswordType = Field(**PASSWORD_FIELD_ARGS)  # type: ignore[misc]
    url: CardSchemaUrlType = Field(**URL_FIELD_ARGS)  # type: ignore[misc]
    description: CardSchemaDescriptionType = Field(**DESCRIPTION_FIELD_ARGS)  # type: ignore[misc]


class UpdateCardRequestSchema(BaseSchema):
    username: CardSchemaUsernameType | None = Field(None, **USERNAME_FIELD_ARGS)  # type: ignore[misc]
    email: CardSchemaEmailType | None = Field(None, **EMAIL_FIELD_ARGS)  # type: ignore[misc]
    password: CardSchemaPasswordType | None = Field(None, **PASSWORD_FIELD_ARGS)  # type: ignore[misc]
    url: CardSchemaUrlType | None = Field(None, **URL_FIELD_ARGS)  # type: ignore[misc]
    description: CardSchemaDescriptionType | None = Field(  # type: ignore[misc]
        None,
        **DESCRIPTION_FIELD_ARGS
    )


class UpdateCardTitleRequestSchema(BaseSchema):
    title: CardSchemaTitleType | None = Field(None, **TITLE_FIELD_ARGS)  # type: ignore[misc]


class CardMetaResponseSchema(BaseSchema):
    card_id: str
    user_id: str
    title: str
    icon_url: str


class CardResponseSchema(BaseSchema):
    meta: CardMetaResponseSchema
    username: str | None = None
    email: str | None = None
    password: str | None = None
    url: str | None = None
    description: str | None = None


class DeletedCardsCountResponseSchema(BaseSchema):
    cards_count: int


class CardInfoResponseSchema(BaseSchema):
    card_id: str
    title: str
    icon_url: str


class CardsInfoResponseSchema(BaseSchema):
    user_id: str
    cards_info: list[CardInfoResponseSchema]

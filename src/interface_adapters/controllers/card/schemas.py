from typing import Any, TypedDict

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    SecretStr,
    field_serializer,
)

from .types import (
    CardSchemaDescriptionType,
    CardSchemaEmailType,
    CardSchemaIDType,
    CardSchemaPasswordType,
    CardSchemaTitleType,
    CardSchemaUrlType,
    CardSchemaUserIDType,
    CardSchemaUsernameType,
)


class FieldArgs(TypedDict, total=False):
    title: str
    description: str
    examples: list[Any]
    min_length: int
    max_length: int


TITLE_FIELD_ARGS: FieldArgs = {
    'title': "Card title",
    'description': "Название карточки пользователя",
    'examples': ['NBStorage'],
    'min_length': 1,
    'max_length': 70,
}
USERNAME_FIELD_ARGS: FieldArgs = {
    'title': "Service username",
    'description': "Имя пользователя от сервиса",
    'examples': ['Notikay'],
    'max_length': 100,
}
EMAIL_FIELD_ARGS: FieldArgs = {
    'title': "Service email",
    'description': "Электронная почта привязанная к сервису",
    'examples': ['notikay@nb.ru'],
    'max_length': 254,
}
PASSWORD_FIELD_ARGS: FieldArgs = {
    'title': "Service password",
    'description': "Пароль от сервиса",
    'examples': ['13062000'],
    'max_length': 256,
}
URL_FIELD_ARGS: FieldArgs = {
    'title': "Service url",
    'description': "URL-адрес сервиса",
    'examples': ['https://www.nbstorage.ru'],
    'max_length': 512,
}
DESCRIPTION_FIELD_ARGS: FieldArgs = {
    'title': "Service description",
    'description': "Описание сервиса",
    'examples': ["Менеджер паролей от инди-студии разработки IT-продуктов 'NotiBit'"],
    'max_length': 1024,
}


class SerializeCardParamsToBytesMixin:
    """
    Миксин сериализации данных карточки пользователя из строки/None в
    байты/None.
    """

    @field_serializer('username', 'email', 'password', 'url', 'description')
    def serialize(
            self,
            value: EmailStr | SecretStr | HttpUrl | str | None,
            _info: Any
    ) -> bytes | None:
        if isinstance(value, SecretStr):
            return value.get_secret_value().encode('utf-8')

        if isinstance(value, (EmailStr, HttpUrl)):
            return str(value).encode('utf-8')

        if isinstance(value, str):
            return value.encode('utf-8')

        return value


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        frozen=True,
        validate_assignment=False,
        strict=True
    )


class CardIDSchema(BaseSchema):
    card_id: CardSchemaIDType = Field(
        title="Card ID",
        description="ID карточки пользователя",
        examples=['91ce3f6a-87f5-4887-acfc-c1528f6048b1']
    )


class UserIDSchema(BaseSchema):
    user_id: CardSchemaUserIDType = Field(
        title="User ID",
        description="ID пользователя",
        examples=['2e7f3e50-30d2-4e8d-baff-1b6df77f267e']
    )


class SelectOneCardSchema(CardIDSchema): ...


class GetCardsInfoSchema(UserIDSchema): ...


class AddCardSchema(UserIDSchema, SerializeCardParamsToBytesMixin):
    title: CardSchemaTitleType = Field(**TITLE_FIELD_ARGS)  # type: ignore[misc]
    username: CardSchemaUsernameType = Field(**USERNAME_FIELD_ARGS)  # type: ignore[misc]
    email: CardSchemaEmailType = Field(**EMAIL_FIELD_ARGS)  # type: ignore[misc]
    password: CardSchemaPasswordType = Field(**PASSWORD_FIELD_ARGS)  # type: ignore[misc]
    url: CardSchemaUrlType = Field(**URL_FIELD_ARGS)  # type: ignore[misc]
    description: CardSchemaDescriptionType = Field(**DESCRIPTION_FIELD_ARGS)  # type: ignore[misc]


class DeleteCardSchema(CardIDSchema): ...


class DeleteAllCardsSchema(UserIDSchema): ...


class UpdateCardSchema(CardIDSchema, SerializeCardParamsToBytesMixin):
    username: CardSchemaUsernameType | None = Field(None, **USERNAME_FIELD_ARGS)  # type: ignore[misc]
    email: CardSchemaEmailType | None = Field(None, **EMAIL_FIELD_ARGS)  # type: ignore[misc]
    password: CardSchemaPasswordType | None = Field(None, **PASSWORD_FIELD_ARGS)  # type: ignore[misc]
    url: CardSchemaUrlType | None = Field(None, **URL_FIELD_ARGS)  # type: ignore[misc]
    description: CardSchemaDescriptionType | None = Field(  # type: ignore[misc]
        None,
        **DESCRIPTION_FIELD_ARGS
    )


class UpdateCardTitleSchema(CardIDSchema):
    title: CardSchemaTitleType | None = Field(None, **TITLE_FIELD_ARGS)  # type: ignore[misc]

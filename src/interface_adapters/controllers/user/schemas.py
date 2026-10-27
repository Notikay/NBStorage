import re
from typing import Any, TypedDict

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    field_serializer,
    field_validator
)
from pydantic_core import PydanticCustomError

from .types import (
    UserSchemaAvatarKeyType,
    UserSchemaIDType,
    UserSchemaLoginType,
    UserSchemaNameType,
    UserSchemaPasswordType,
    UserSchemaTimeBlockType,
)


class FieldArgs(TypedDict, total=False):
    title: str
    description: str
    examples: list[Any]
    pattern: str
    ge: float
    multiple_of: float
    min_length: int
    max_length: int


NAME_FIELD_ARGS: FieldArgs = {
    'title': "User name",
    'description': "Имя пользователя",
    'examples': ['BANKSY', 'Taste', 'Ben37', 'stash', 'Bakeroner'],
    'min_length': 2,
    'max_length': 50
}
AVATAR_KEY_FIELD_ARGS: FieldArgs = {
    'title': "Avatar key",
    'description': "Ключ аватарки пользователя",
    'examples': [
        'SAMO.png',
        '/rest/in/peace/паша183.jpg',
        './rest/in/peace/super158.jpeg',
        '../rest/in/peace/zoom.webp'
    ],
    'max_length': 255
}
TIME_BLOCK_FIELD_ARGS: FieldArgs = {
    'title': "Session time block",
    'description': "Время блокировки сессии пользователя",
    'examples': [0, 8, 24, 2000],
    'ge': 0,
    'multiple_of': 8
}
LOGIN_FIELD_ARGS: FieldArgs = {
    'title': "User login",
    'description': "Логин пользователя",
    'examples': ['tgk', 'babangida', 'good_hash_production'],
    'pattern': r"^[a-z0-9_]+$",
    'min_length': 3,
    'max_length': 30
}
PASSWORD_FIELD_ARGS: FieldArgs = {
    'title': "User password",
    'description': "Пароль пользователя",
    'examples': ['password', '12345678', 'qwerty12345678'],
    'min_length': 8,
    'max_length': 128
}

PASSWORD_PATTERN = re.compile(r"^[A-Za-z0-9!@#$%^&*_=+|\\\[\]{};:/?.><()-]+$")


class SerializeUserPasswordToBytesMixin:
    """
    Миксин сериализации пароля пользователя из строки/None в байты/None.
    """

    @field_serializer('password')
    def serialize(self, value: SecretStr | None, _info: Any) -> bytes | None:
        if value is None:
            return None
        return value.get_secret_value().encode('utf-8')


class ValidateUserPasswordPatternMixin:
    """Миксин соответствия пароля пользователя шаблону поля."""

    @field_validator('password', mode='before')
    def validate_password(cls, value: SecretStr | None) -> SecretStr:
        if (value is not None) and (not PASSWORD_PATTERN.match(str(value))):
            raise PydanticCustomError(
                "password_pattern_mismatch",
                "В пароле есть символы, которые не поддерживаются!"
            )
        return value


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        str_strip_whitespace=True,
        frozen=True,
        validate_assignment=False,
        strict=True
    )


class UserIDSchema(BaseSchema):
    """Миксин с ID пользователя для модели валидации данных."""
    user_id: UserSchemaIDType = Field(
        title="User ID",
        description="ID пользователя",
        examples=['2e7f3e50-30d2-4e8d-baff-1b6df77f267e']
    )


class SelectOneUserSchema(UserIDSchema): ...


class RegistrationUserSchema(
    BaseSchema,
    ValidateUserPasswordPatternMixin,
    SerializeUserPasswordToBytesMixin
):
    name: UserSchemaNameType = Field(**NAME_FIELD_ARGS)  # type: ignore[misc]
    time_block: UserSchemaTimeBlockType = Field(**TIME_BLOCK_FIELD_ARGS)  # type: ignore[misc]
    login: UserSchemaLoginType = Field(**LOGIN_FIELD_ARGS)  # type: ignore[misc]
    password: UserSchemaPasswordType = Field(**PASSWORD_FIELD_ARGS)  # type: ignore[misc]


class DeleteUserSchema(UserIDSchema): ...


class UpdateUserSchema(
    UserIDSchema,
    ValidateUserPasswordPatternMixin,
    SerializeUserPasswordToBytesMixin
):
    login: UserSchemaLoginType | None = Field(None, **LOGIN_FIELD_ARGS)  # type: ignore[misc]
    password: UserSchemaPasswordType | None = Field(None, **PASSWORD_FIELD_ARGS)  # type: ignore[misc]


class UpdateUserSettingsSchema(UserIDSchema):
    name: UserSchemaNameType | None = Field(None, **NAME_FIELD_ARGS)  # type: ignore[misc]
    avatar_key: UserSchemaAvatarKeyType | None = Field(None, **AVATAR_KEY_FIELD_ARGS)  # type: ignore[misc]
    time_block: UserSchemaTimeBlockType | None = Field(None, **TIME_BLOCK_FIELD_ARGS)  # type: ignore[misc]

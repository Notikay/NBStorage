from pydantic import Field

from interface_adapters.controllers.user.schemas import (
    NAME_FIELD_ARGS,
    TIME_BLOCK_FIELD_ARGS,
    LOGIN_FIELD_ARGS,
    PASSWORD_FIELD_ARGS,
    RegistrationUserSchema,
)
from interface_adapters.controllers.user.types import (
    UserSchemaNameType,
    UserSchemaTimeBlockType,
    UserSchemaLoginType,
    UserSchemaPasswordType,
)

from .base import BaseSchema


class RegistrationUserRequestSchema(RegistrationUserSchema): ...


class UpdateUserRequestSchema(BaseSchema):
    login: UserSchemaLoginType | None = Field(None, **LOGIN_FIELD_ARGS)  # type: ignore[misc]
    password: UserSchemaPasswordType | None = Field(None, **PASSWORD_FIELD_ARGS)  # type: ignore[misc]


class UpdateUserSettingsRequestSchema(BaseSchema):
    name: UserSchemaNameType | None = Field(None, **NAME_FIELD_ARGS)  # type: ignore[misc]
    time_block: UserSchemaTimeBlockType | None = Field(None, **TIME_BLOCK_FIELD_ARGS)  # type: ignore[misc]


class UserMetaResponseSchema(BaseSchema):
    user_id: str
    name: str
    avatar_url: str
    time_block: int


class UserResponseSchema(BaseSchema):
    meta: UserMetaResponseSchema
    login: str


class DeletedUsersCountResponseSchema(BaseSchema):
    users_count: int


class UserInfoResponseSchema(BaseSchema):
    user_id: str
    name: str
    avatar_url: str
    login: str


class UsersInfoResponseSchema(BaseSchema):
    users_info: list[UserInfoResponseSchema]

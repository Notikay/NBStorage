from dataclasses import dataclass

from domain.entities.user.types import (
    UserLoginType,
    UserMetaIDType,
    UserMetaNameType,
    UserMetaTimeBlockType,
    UserMetaUpdNameType,
    UserMetaUpdTimeBlockType,
    UserPasswordType,
    UserUpdLoginType,
    UserUpdPasswordType,
)


@dataclass(frozen=True, slots=True)
class ChooseUserCommand:
    user_id: UserMetaIDType


@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    name: UserMetaNameType
    time_block: UserMetaTimeBlockType
    login: UserLoginType
    password: UserPasswordType


@dataclass(frozen=True, slots=True)
class DeleteUserCommand:
    user_id: UserMetaIDType


@dataclass(frozen=True, slots=True)
class UpdateUserCommand:
    user_id: UserMetaIDType
    login: UserUpdLoginType = None
    password: UserUpdPasswordType = None


@dataclass(frozen=True, slots=True)
class UpdateUserMetaCommand:
    user_id: UserMetaIDType
    name: UserMetaUpdNameType = None
    time_block: UserMetaUpdTimeBlockType = None

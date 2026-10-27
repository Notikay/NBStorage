from dataclasses import dataclass

from infrastructure.database.models.types import (
    UserModelAvatarKeyType,
    UserModelIDType,
    UserModelLoginType,
    UserModelNameType,
)


@dataclass(frozen=True, slots=True)
class UserInfoProjection:
    user_id: UserModelIDType
    name: UserModelNameType
    avatar_key: UserModelAvatarKeyType
    login: UserModelLoginType


@dataclass(frozen=True, slots=True)
class UsersInfoCollectionProjection:
    users_info: list[UserInfoProjection]

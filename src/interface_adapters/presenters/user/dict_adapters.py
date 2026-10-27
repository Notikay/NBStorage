from collections.abc import Sequence
from typing import TypedDict

from domain.entities.user import User, UserMeta
from domain.interfaces import ObjectStore
from domain.use_cases.user.types import UsersCountType
from infrastructure.database.query_services.user.projections import (
    UserInfoProjection,
    UsersInfoCollectionProjection
)

from ..mixins import ShowErrorMapMixin
from ..views import MapView

type UserIDResultType = str
type UserNameResultType = str
type UserAvatarURLResultType = str
type UserLoginResultType = str


class UserMetaDict(TypedDict):
    user_id: UserIDResultType
    name: UserNameResultType
    avatar_url: UserAvatarURLResultType
    time_block: int


class UserDict(TypedDict):
    meta: UserMetaDict
    login: UserLoginResultType


class UsersCountDict(TypedDict):
    users_count: UsersCountType


class UserInfoDict(TypedDict):
    user_id: UserIDResultType
    name: UserNameResultType
    avatar_url: UserAvatarURLResultType
    login: UserLoginResultType


class UserDictAdapter(ShowErrorMapMixin):
    """Адаптер пользователя в словарь."""

    def __init__(self, object_store: ObjectStore) -> None:
        self.__object_store = object_store

    def show_success(self, result: User | Sequence[User]) -> MapView:
        if isinstance(result, Sequence):
            result_list_dict: list[UserDict] = [
                self.__convert_user_to_dict(user)
                for user in result
            ]
            return MapView("Перечень пользователей успешно получен!", result_list_dict)

        result_dict = self.__convert_user_to_dict(result)
        return MapView("Пользователь успешно получен!", result_dict)

    def __convert_user_to_dict(self, user: User) -> UserDict:
        user_id = str(user.meta.user_id)
        avatar_url = self.__object_store.get_url(user.meta.avatar_key, private=True) \
            if user.meta.avatar_key \
            else self.__object_store.get_url(user.meta.get_default_avatar_key())

        return {
            'meta': {
                'user_id': user_id,
                'name': user.meta.name,
                'avatar_url': avatar_url,
                'time_block': user.meta.time_block
            },
            'login': user.login
        }


class UsersCountDictAdapter(ShowErrorMapMixin):
    """Адаптер количества пользователей в словарь."""

    def show_success(self, result: UsersCountType) -> MapView:
        result_dict = {'users_count': result}
        return MapView("Количество пользователей успешно получено!", result_dict)


class UsersInfoDictAdapter(ShowErrorMapMixin):
    """Адаптер информации о пользователе в словарь."""

    def __init__(self, object_store: ObjectStore) -> None:
        self.__object_store = object_store

    def show_success(self, result: UsersInfoCollectionProjection) -> MapView:
        users_info = list(map(self.__convert_user_info_to_dict, result.users_info))
        result_dict = {'users_info': users_info}
        return MapView("Информация о пользователе успешно получена!", result_dict)

    def __convert_user_info_to_dict(
            self,
            user_info: UserInfoProjection
    ) -> UserInfoDict:
        user_id = str(user_info.user_id)
        avatar_url = self.__object_store.get_url(user_info.avatar_key, private=True) \
            if user_info.avatar_key \
            else self.__object_store.get_url(UserMeta.get_default_avatar_key())

        return {
            'user_id': user_id,
            'name': user_info.name,
            'avatar_url': avatar_url,
            'login': user_info.login
        }

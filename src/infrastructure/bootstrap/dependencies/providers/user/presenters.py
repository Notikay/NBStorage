from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from domain.entities.user import User
from domain.interfaces import NonePresenter, ObjectStore, ResultPresenter
from domain.use_cases.user.types import UsersCountType
from infrastructure.database.query_services.user.projections import (
    UsersInfoCollectionProjection,
)
from interface_adapters.presenters import NoneMapAdapter
from interface_adapters.presenters.user import (
    UserDictAdapter,
    UsersCountDictAdapter,
    UsersInfoDictAdapter,
)
from interface_adapters.presenters.views import MapView

type MinioPortType = Annotated[ObjectStore, FromComponent('minio')]


class UserNonePresenterProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_none_map(self) -> NonePresenter[MapView]:
        return NoneMapAdapter()


class UserPresenterProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_minio_user_dict(
            self,
            object_store: MinioPortType
    ) -> ResultPresenter[User, MapView]:
        return UserDictAdapter(object_store)


class UsersInfoProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_minio_users_info_dict(
            self,
            object_store: MinioPortType
    ) -> ResultPresenter[UsersInfoCollectionProjection, MapView]:
        return UsersInfoDictAdapter(object_store)


class UsersCountProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_users_count_dict(self) -> ResultPresenter[UsersCountType, MapView]:
        return UsersCountDictAdapter()

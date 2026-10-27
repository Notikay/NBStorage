from typing import Annotated

from dishka import Provider, Scope, provide, FromComponent

from domain.entities.user import User
from domain.interfaces import (
    CMDUseCase,
    DataController,
    NoneController,
    NonePresenter,
    NoneUseCase,
    ResultPresenter,
)
from domain.interfaces.user import UserQueryService
from domain.use_cases.user.commands import (
    ChooseUserCommand,
    CreateUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
    UpdateUserMetaCommand,
)
from domain.use_cases.user.types import UsersCountType
from infrastructure.database.query_services.user.projections import (
    UsersInfoCollectionProjection,
)
from interface_adapters.controllers.user import (
    DeleteAllUsers,
    DeleteUser,
    GetUsersInfo,
    RegistrationUser,
    SelectOneUser,
    UpdateUser,
    UpdateUserSettings,
)
from interface_adapters.controllers.user.schemas import (
    DeleteUserSchema,
    RegistrationUserSchema,
    SelectOneUserSchema,
    UpdateUserSchema,
    UpdateUserSettingsSchema,
)
from interface_adapters.presenters.views import MapView


class UserControllerProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_registration_user(
            self,
            use_case: CMDUseCase[CreateUserCommand, User],
            presenter: ResultPresenter[User, MapView]
    ) -> DataController[RegistrationUserSchema, MapView]:
        return RegistrationUser(use_case, presenter)

    @provide(provides=Annotated[
        NoneController[MapView],
        FromComponent('delete_all_users')
    ])
    def provide_delete_all_users(
            self,
            use_case: NoneUseCase[UsersCountType],
            presenter: ResultPresenter[UsersCountType, MapView]
    ) -> NoneController[MapView]:
        return DeleteAllUsers(use_case, presenter)

    @provide
    def provide_delete_user(
            self,
            use_case: CMDUseCase[DeleteUserCommand, None],
            presenter: NonePresenter[MapView]
    ) -> DataController[DeleteUserSchema, MapView]:
        return DeleteUser(use_case, presenter)

    @provide(provides=Annotated[
        NoneController[MapView],
        FromComponent('get_users_info')
    ])
    def provide_get_users_info(
            self,
            query_service: UserQueryService[UsersInfoCollectionProjection],
            presenter: ResultPresenter[UsersInfoCollectionProjection, MapView]
    ) -> NoneController[MapView]:
        return GetUsersInfo(query_service, presenter)

    @provide
    def provide_select_one_user(
            self,
            use_case: CMDUseCase[ChooseUserCommand, User],
            presenter: ResultPresenter[User, MapView]
    ) -> DataController[SelectOneUserSchema, MapView]:
        return SelectOneUser(use_case, presenter)

    @provide
    def provide_update_user(
            self,
            use_case: CMDUseCase[UpdateUserCommand, User],
            presenter: ResultPresenter[User, MapView]
    ) -> DataController[UpdateUserSchema, MapView]:
        return UpdateUser(use_case, presenter)

    @provide
    def provide_update_user_settings(
            self,
            use_case: CMDUseCase[UpdateUserMetaCommand, User],
            presenter: ResultPresenter[User, MapView]
    ) -> DataController[UpdateUserSettingsSchema, MapView]:
        return UpdateUserSettings(use_case, presenter)

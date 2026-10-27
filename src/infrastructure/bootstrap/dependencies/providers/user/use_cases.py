from dishka import Provider, Scope, provide

from domain.entities.user import User
from domain.interfaces import CMDUseCase, NoneUseCase
from domain.interfaces.user import UserUnitOfWork
from domain.use_cases.user import (
    ChooseUser,
    CreateUser,
    DeleteAllUsers,
    DeleteUser,
    UpdateUser,
    UpdateUserMeta,
)
from domain.use_cases.user.commands import (
    ChooseUserCommand,
    CreateUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
    UpdateUserMetaCommand,
)
from domain.use_cases.user.types import UsersCountType


class UserUseCaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_choose_user(
            self,
            uow: UserUnitOfWork
    ) -> CMDUseCase[ChooseUserCommand, User]:
        return ChooseUser(uow)

    @provide
    def provide_create_user(
            self,
            uow: UserUnitOfWork
    ) -> CMDUseCase[CreateUserCommand, User]:
        return CreateUser(uow)

    @provide
    def provide_delete_user(
            self,
            uow: UserUnitOfWork
    ) -> CMDUseCase[DeleteUserCommand, None]:
        return DeleteUser(uow)

    @provide
    def provide_delete_all_users(
            self,
            uow: UserUnitOfWork
    ) -> NoneUseCase[UsersCountType]:
        return DeleteAllUsers(uow)

    @provide
    def provide_update_user(
            self,
            uow: UserUnitOfWork
    ) -> CMDUseCase[UpdateUserCommand, User]:
        return UpdateUser(uow)

    @provide
    def provide_update_user_meta(
            self,
            uow: UserUnitOfWork
    ) -> CMDUseCase[UpdateUserMetaCommand, User]:
        return UpdateUserMeta(uow)

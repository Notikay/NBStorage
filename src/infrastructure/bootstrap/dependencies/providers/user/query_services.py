from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session

from domain.interfaces.user import UserQueryService
from infrastructure.database.query_services.user import UserProvider
from infrastructure.database.query_services.user.projections import (
    UsersInfoCollectionProjection,
)


class UserQueryServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_user_provider(
            self,
            session: Session
    ) -> UserQueryService[UsersInfoCollectionProjection]:
        return UserProvider(session)

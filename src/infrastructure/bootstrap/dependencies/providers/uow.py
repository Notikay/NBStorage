from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.orm import Session, sessionmaker

from domain.interfaces.card import CardUnitOfWork
from domain.interfaces.user import UserUnitOfWork
from infrastructure.database.uow import TransactionManager


class UnitOfWorkProvider(Provider):
    scope = Scope.REQUEST

    @provide(provides=AnyOf[CardUnitOfWork, UserUnitOfWork])
    def provide_transaction_manager(
            self,
            session_factory: sessionmaker[Session]
    ) -> TransactionManager:
        return TransactionManager(session_factory)

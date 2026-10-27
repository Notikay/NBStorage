from collections.abc import Iterator

from dishka import Provider, Scope, provide
from minio import Minio
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from infrastructure.config.settings import DBSettings, StoreSettings


class ConnectionDBProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_sqlalchemy_engine(self, db_settings: DBSettings) -> Engine:
        return create_engine(
            db_settings.url,
            echo=False,
            pool_size=10,
            max_overflow=20,
            pool_timeout=5,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={
                "connect_timeout": 3,
                "options": "-c statement_timeout=3000",
            },
        )

    @provide
    def provide_sqlalchemy_session_factory(
            self,
            engine: Engine
    ) -> sessionmaker[Session]:
        return sessionmaker(bind=engine, expire_on_commit=True)

    @provide(provides=Session, scope=Scope.REQUEST)
    def provide_sqlalchemy_session(
            self,
            session_factory: sessionmaker[Session]
    ) -> Iterator[Session]:
        with session_factory() as session:
            yield session


class ConnectionStoreProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_minio_client(self, store_settings: StoreSettings) -> Minio:
        return Minio(
            store_settings.endpoint,
            store_settings.access_key,
            store_settings.secret_key,
            secure=store_settings.secure,
        )

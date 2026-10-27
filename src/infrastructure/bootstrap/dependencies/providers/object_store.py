from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide
from minio import Minio

from domain.interfaces import ObjectStore
from infrastructure.config.settings import StoreSettings
from infrastructure.object_stores import MinIOPort


class ObjectStoreProvider(Provider):
    scope = Scope.APP

    @provide(provides=Annotated[ObjectStore, FromComponent('minio')])
    def provide_minio_port(
            self,
            client: Minio,
            store_settings: StoreSettings
    ) -> ObjectStore:
        return MinIOPort(
            client,
            store_settings.public_bucket_name,
            store_settings.private_bucket_name,
            store_settings.public_url
        )

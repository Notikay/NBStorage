from io import BytesIO

from minio import Minio
from minio.error import S3Error

from .exceptions import DeleteFileError, SaveFileError

type BucketNameType = str
type KeyType = str


class MinIOPort:

    def __init__(
            self,
            client: Minio,
            public_bucket_name: BucketNameType,
            private_bucket_name: BucketNameType,
            public_url: str
    ) -> None:
        self.__client = client
        self.__public_bucket_name = public_bucket_name
        self.__private_bucket_name = private_bucket_name
        self.__public_url = public_url.rstrip('/')

        self.__create_bucket_if_not_exist(self.__public_bucket_name)
        self.__create_bucket_if_not_exist(self.__private_bucket_name)

    def save(self, key: KeyType, content: bytes, content_type: str) -> None:
        try:
            self.__client.put_object(
                bucket_name=self.__private_bucket_name,
                object_name=key,
                data=BytesIO(content),
                length=len(content),
                content_type=content_type,
            )
        except S3Error as e:
            raise SaveFileError(key) from e

    def delete(self, key: KeyType) -> None:
        try:
            self.__client.remove_object(self.__private_bucket_name, key)
        except S3Error as e:
            raise DeleteFileError(key) from e

    def get_url(self, key: KeyType, private: bool = False) -> str:
        bucket_name = self.__private_bucket_name \
            if private else self.__public_bucket_name
        return f"{self.__public_url}/{bucket_name}/{key}"

    def __create_bucket_if_not_exist(self, bucket_name: BucketNameType) -> None:
        if not self.__client.bucket_exists(bucket_name):
            self.__client.make_bucket(bucket_name)

import json
import mimetypes
import time
from pathlib import Path

import structlog
from minio import Minio

from domain.entities.card import CardMeta
from domain.entities.user import UserMeta
from infrastructure.config.settings import StoreSettings, load_settings

logger = structlog.getLogger(__name__)

type BucketNameType = str

DEFAULT_ASSETS = {
    CardMeta.get_default_icon_key(): Path(
        "src/infrastructure/static/card/icons/default.webp"
    ),
    UserMeta.get_default_avatar_key(): Path(
        "src/infrastructure/static/user/avatars/default.webp"
    ),
}


def _waiting_for_minio(client: Minio, retries: int = 20) -> None:
    while retries > 0:
        logger.debug("waiting_for_minio", retries=retries)
        try:
            client.list_buckets()
            return
        except Exception:
            retries -= 1
            time.sleep(1)

    logger.error("minio_not_ready")
    raise RuntimeError("MinIO not ready!")

def _create_bucket_if_not_exist(client: Minio, bucket_name: BucketNameType) -> None:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        logger.debug("bucket_created", bucket_name=bucket_name)
    else:
        logger.debug("bucket_already_exists", bucket_name=bucket_name)

def _ensure_public_read_policy(client: Minio, bucket_name: BucketNameType) -> None:
    policy = {
        'Version': "2012-10-17",
        'Statement': [
            {
                'Sid': "AllowAnonymousRead",
                'Effect': "Allow",
                'Principal': {'AWS': ["*"]},
                'Action': ["s3:GetObject"],
                'Resource': [f"arn:aws:s3:::{bucket_name}/*", ]
            },
        ],
    }
    client.set_bucket_policy(bucket_name, json.dumps(policy))
    logger.debug("set_public_read_policy", bucket_name=bucket_name)

def _object_exist(client: Minio, bucket_name: BucketNameType, object_name: str) -> bool:
    try:
        client.stat_object(bucket_name, object_name)
        return True
    except Exception:
        return False

def main(store_settings: StoreSettings) -> None:
    client = Minio(
        store_settings.endpoint,
        store_settings.access_key,
        store_settings.secret_key,
        secure=store_settings.secure,
    )

    _waiting_for_minio(client)

    _create_bucket_if_not_exist(client, store_settings.public_bucket_name)
    _create_bucket_if_not_exist(client, store_settings.private_bucket_name)

    _ensure_public_read_policy(client, store_settings.public_bucket_name)

    for object_name, local_path in DEFAULT_ASSETS.items():
        content_type, _ = mimetypes.guess_type(local_path)
        if not _object_exist(client, store_settings.public_bucket_name, object_name):
            try:
                client.fput_object(
                    bucket_name=store_settings.public_bucket_name,
                    object_name=object_name,
                    file_path=str(local_path),
                    content_type=content_type or 'application/octet-stream',
                )
            except Exception as e:
                logger.exception(
                    "failed_to_upload_minio_asset",
                    object_name=object_name,
                    local_path=local_path,
                    error=str(e)
                )
                raise


if __name__ == '__main__':
    settings = load_settings()
    main(settings.store)

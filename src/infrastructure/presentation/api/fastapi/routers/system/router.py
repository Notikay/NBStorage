from datetime import UTC, datetime

import structlog
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from minio import Minio
from sqlalchemy import text
from sqlalchemy.orm import Session

from infrastructure.config.settings import load_settings

from ..schemas.system import (
    HealthComponentsSchema,
    HealthResponseSchema,
    RootResponseSchema,
)
from .exceptions import DBConnectionError, StoreConnectionError

logger = structlog.getLogger(__name__)

router = APIRouter(tags=["System"], )

settings = load_settings()


@router.get(
    "/",
    response_model=RootResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Проверка доступа",
)
def root() -> RootResponseSchema:
    return RootResponseSchema(
        project=settings.api.title,
        summary=settings.api.summary,
        version=settings.api.version,
        status='alive',
        timestamp=datetime.now(UTC).isoformat()
    )


@router.get(
    "/health",
    response_model=HealthResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Проверка статуса",
)
@inject
def health(
        minio_client: FromDishka[Minio],
        db_session: FromDishka[Session],
) -> HealthResponseSchema:
    store_status = True
    db_status = True

    try:
        minio_client.list_buckets()
    except Exception:
        logger.exception(
            StoreConnectionError.log_event,
            error=str(StoreConnectionError),
            error_code=StoreConnectionError.code,
        )
        store_status = False

    try:
        db_session.execute(text("SELECT 1"))
    except Exception:
        logger.exception(
            DBConnectionError.log_event,
            error=str(DBConnectionError),
            error_code=DBConnectionError.code,
        )
        db_status = False

    return HealthResponseSchema(
        status="ready" if store_status and db_status else "not ready",
        components=HealthComponentsSchema(
            store="ok" if store_status else "down",
            database="ok" if db_status else "down"
        )
    )

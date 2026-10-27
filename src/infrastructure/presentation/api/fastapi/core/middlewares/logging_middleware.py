import time
import uuid
from typing import Any

import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Any) -> Any:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.url.path,
            method=request.method,
        )

        start_time = time.perf_counter()
        try:
            response = await call_next(request)

            duration = time.perf_counter() - start_time
            logger.info(
                'request_completed',
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
            )

            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            duration = time.perf_counter() - start_time
            logger.exception(
                'request_failed',
                error=str(e),
                duration_ms=round(duration * 1000, 2),
            )
            raise
        finally:
            structlog.contextvars.clear_contextvars()

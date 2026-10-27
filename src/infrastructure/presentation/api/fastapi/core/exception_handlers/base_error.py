import structlog
from fastapi import Request
from fastapi.responses import JSONResponse

from shared.errors import ERROR_STATUS_MAP, BaseError

logger = structlog.getLogger(__name__)


def base_error_handler(_request: Request, exc: BaseError) -> JSONResponse:
    logger.error(exc.log_event, error=str(exc), error_code=exc.code)
    return JSONResponse(
        status_code=ERROR_STATUS_MAP[exc.code],
        content={'code': exc.code, 'message': exc.message},
    )

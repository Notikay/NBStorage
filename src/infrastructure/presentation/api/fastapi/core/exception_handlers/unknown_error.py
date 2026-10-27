import structlog
from fastapi import Request
from fastapi.responses import JSONResponse

from shared.errors import ERROR_STATUS_MAP, UnknownError

logger = structlog.getLogger(__name__)


def unknown_error_handler(_request: Request, _exc: Exception) -> JSONResponse:
    exc = UnknownError("Неизвестная ошибка!")
    logger.exception(exc.log_event, error=str(exc), error_code=exc.code)
    return JSONResponse(
        status_code=ERROR_STATUS_MAP[exc.code],
        content={'code': exc.code, 'message': exc.message},
    )

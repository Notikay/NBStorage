import logging
import sys
from typing import Any, Literal

import orjson
import structlog


def _json_serializer(obj: object, **kwargs: Any) -> str:  # noqa: ARG001
    return orjson.dumps(obj).decode("utf-8")


def configure_logging(
        environment: Literal['dev', 'prod'] = 'prod',
        debug: bool = False
) -> None:
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.processors.StackInfoRenderer(),
    ]

    # Перехват логов зависимостей.
    handler = logging.StreamHandler(sys.stdout)
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,  # type: ignore[arg-type]
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(
                serializer=_json_serializer
            ) if environment == 'prod'
            else structlog.dev.ConsoleRenderer(),
        ]
    )
    handler.setFormatter(formatter)

    # Сброс корневого логгера.
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]

    # Настройка логгера в зависимости от контура.
    if environment == 'prod':
        processors = [
            *shared_processors,
            structlog.processors.dict_tracebacks,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ]
        root_logger.setLevel(logging.INFO)
    else:
        processors = [
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer()
        ]
        root_logger.setLevel(logging.DEBUG if debug else logging.INFO)

    structlog.configure(
        processors,  # type: ignore[arg-type]
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    for logger_name in ('uvicorn', 'uvicorn.access', 'uvicorn.error'):
        logging.getLogger(logger_name).handlers = []
        logging.getLogger(logger_name).propagate = True

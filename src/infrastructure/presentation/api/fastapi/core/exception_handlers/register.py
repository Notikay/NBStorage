from fastapi import FastAPI

from shared.errors import BaseError

from .base_error import base_error_handler
from .unknown_error import unknown_error_handler

HANDLERS = {
    BaseError: base_error_handler,
    Exception: unknown_error_handler,
}


def register_exception_handlers(app: FastAPI) -> None:
    for e, handler in HANDLERS.items():
        app.add_exception_handler(e, handler)  # type: ignore[arg-type]

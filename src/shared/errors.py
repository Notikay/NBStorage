from enum import StrEnum, auto
from typing import Any, override

type MessageType = str
type LogEventType = str


class ErrorCode(StrEnum):

    @override
    @staticmethod
    def _generate_next_value_(
            name: Any,
            start: Any,
            count: Any,
            last_values: Any
    ) -> Any:
        return name

    VALIDATION_ERROR = auto()
    NOT_FOUND_ERROR = auto()
    OPERATION_ERROR = auto()
    STORAGE_ERROR = auto()
    STORE_ERROR = auto()
    DATABASE_ERROR = auto()
    INTERNAL_ERROR = auto()
    UNKNOWN_ERROR = auto()


ERROR_STATUS_MAP = {
    ErrorCode.VALIDATION_ERROR: 422,
    ErrorCode.NOT_FOUND_ERROR: 404,
    ErrorCode.OPERATION_ERROR: 409,
    ErrorCode.STORAGE_ERROR: 507,
    ErrorCode.STORE_ERROR: 507,
    ErrorCode.DATABASE_ERROR: 500,
    ErrorCode.INTERNAL_ERROR: 500,
    ErrorCode.UNKNOWN_ERROR: 500,
}


class BaseError(Exception):
    def __init__(self, message: MessageType, code: ErrorCode) -> None:
        self.__message = message
        self.__code = code

        super().__init__(message)

    @property
    def message(self) -> MessageType:
        return self.__message

    @property
    def code(self) -> ErrorCode:
        return self.__code

    @property
    def log_event(self) -> LogEventType:
        return "base_error"


class ValidationError(BaseError):
    def __init__(self, message: MessageType) -> None:
        super().__init__(message, ErrorCode.VALIDATION_ERROR)

    @override
    @property
    def log_event(self) -> LogEventType:
        return "validation_error"


class NotFoundError(BaseError):
    def __init__(self, message: MessageType) -> None:
        super().__init__(message, ErrorCode.NOT_FOUND_ERROR)

    @override
    @property
    def log_event(self) -> LogEventType:
        return "not_found_error"


class OperationError(BaseError):
    def __init__(self, message: MessageType) -> None:
        super().__init__(message, ErrorCode.OPERATION_ERROR)

    @override
    @property
    def log_event(self) -> LogEventType:
        return "operation_error"


class StorageError(BaseError):
    def __init__(self, message: MessageType) -> None:
        super().__init__(message, ErrorCode.STORAGE_ERROR)

    @override
    @property
    def log_event(self) -> LogEventType:
        return "storage_error"


class StoreError(BaseError):
    def __init__(self, message: MessageType) -> None:
        super().__init__(message, ErrorCode.STORE_ERROR)

    @override
    @property
    def log_event(self) -> LogEventType:
        return "store_error"


class DataBaseError(BaseError):
    def __init__(self, message: MessageType) -> None:
        super().__init__(message, ErrorCode.DATABASE_ERROR)

    @override
    @property
    def log_event(self) -> LogEventType:
        return "database_error"


class InternalError(BaseError):
    def __init__(self, message: MessageType) -> None:
        super().__init__(message, ErrorCode.INTERNAL_ERROR)

    @override
    @property
    def log_event(self) -> LogEventType:
        return "internal_error"


class UnknownError(BaseError):
    def __init__(self, message: MessageType) -> None:
        super().__init__(message,  ErrorCode.UNKNOWN_ERROR)

    @override
    @property
    def log_event(self) -> LogEventType:
        return "unknown_error"

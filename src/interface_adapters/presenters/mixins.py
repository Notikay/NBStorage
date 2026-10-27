from shared.errors import ErrorCode, MessageType

from .views import MapView


class ShowErrorMapMixin:
    """Миксин предоставления ошибки операции."""

    @staticmethod
    def show_error(message: MessageType, code: ErrorCode) -> MapView:
        return MapView(message, None, code)

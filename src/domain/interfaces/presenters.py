from typing import Protocol

from shared.errors import ErrorCode, MessageType


class ErrorPresenter[ViewT](Protocol):
    @staticmethod
    def show_error(message: MessageType, code: ErrorCode) -> ViewT: ...


class ResultPresenter[ResultT, ViewT](ErrorPresenter[ViewT], Protocol):
    def show_success(self, result: ResultT) -> ViewT: ...


class NonePresenter[ViewT](ErrorPresenter[ViewT], Protocol):
    @staticmethod
    def show_success() -> ViewT: ...

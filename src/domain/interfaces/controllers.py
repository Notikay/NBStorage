from typing import Protocol


class DataController[SchemaT, ViewT](Protocol):
    def __call__(self, data: SchemaT) -> ViewT: ...


class NoneController[ViewT](Protocol):
    def __call__(self) -> ViewT: ...

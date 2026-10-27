from typing import Protocol


class CMDUseCase[CommandT, ResultT](Protocol):
    def __call__(self, cmd: CommandT) -> ResultT: ...


class NoneUseCase[ResultT](Protocol):
    def __call__(self) -> ResultT: ...

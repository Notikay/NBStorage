from types import TracebackType
from typing import Mapping, Any, Callable

type MapType = Mapping[str, Any]
type CheckParamFnType = Callable[[Any], None]

type UOWErrorType = type[BaseException] | None
type UOWValueErrorType = BaseException | None
type UOWTracebackErrorType = TracebackType | None

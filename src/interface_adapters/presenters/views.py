from collections.abc import Mapping, Sequence
from dataclasses import dataclass

type MessageType = str
type MapType = Mapping[str, object]
type CodeType = str


@dataclass(frozen=True, slots=True)
class MapView:
    message: MessageType = "Операция прошла успешно!"
    result: MapType | Sequence[MapType] | None = None
    code: CodeType = 'SUCCESS'

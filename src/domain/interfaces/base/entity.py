from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .base_types import MapType, CheckParamFnType


class AbstractEntity[T: MapType](ABC):
    """Абстрактный класс сущности."""

    @abstractmethod
    def to_dict(self) -> T:
        pass

    def _update_field(
            self,
            param_field_name: str,
            value: Any,
            check_param_fn: CheckParamFnType
    ) -> None:
        if value is not None:
            check_param_fn(value)
            setattr(self, param_field_name, value)

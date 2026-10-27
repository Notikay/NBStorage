from collections.abc import Callable

type CheckParamFnType = Callable[..., None]


class UpdateEntityParamMixin:
    """Миксин обновления поля сущности."""

    def _update_field(
            self,
            param_field_name: str,
            value: object,
            check_param_fn: CheckParamFnType
    ) -> None:
        if value is not None:
            check_param_fn(value)
            setattr(self, param_field_name, value)

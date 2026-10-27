from .mixins import ShowErrorMapMixin
from .views import MapView


class NoneMapAdapter(ShowErrorMapMixin):
    """Адаптер пустого результата в словарь."""

    @staticmethod
    def show_success() -> MapView:
        return MapView()

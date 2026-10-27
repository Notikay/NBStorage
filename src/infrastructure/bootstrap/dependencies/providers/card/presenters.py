from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from domain.entities.card import Card
from domain.interfaces import NonePresenter, ObjectStore, ResultPresenter
from domain.use_cases.card.types import CardsCountType
from infrastructure.database.query_services.card.projections import (
    CardsInfoCollectionProjection,
)
from interface_adapters.presenters import NoneMapAdapter
from interface_adapters.presenters.card import (
    CardDictAdapter,
    CardsCountDictAdapter,
    CardsInfoDictAdapter,
)
from interface_adapters.presenters.views import MapView

type MinioPortType = Annotated[ObjectStore, FromComponent('minio')]


class CardNonePresenterProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_none_map(self) -> NonePresenter[MapView]:
        return NoneMapAdapter()


class CardPresenterProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_minio_card_dict(
            self,
            object_store: MinioPortType
    ) -> ResultPresenter[Card, MapView]:
        return CardDictAdapter(object_store)


class CardInfoProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_minio_cards_info_dict(
            self,
            object_store: MinioPortType
    ) -> ResultPresenter[CardsInfoCollectionProjection, MapView]:
        return CardsInfoDictAdapter(object_store)


class CardsCountProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_cards_count_dict(self) -> ResultPresenter[CardsCountType, MapView]:
        return CardsCountDictAdapter()

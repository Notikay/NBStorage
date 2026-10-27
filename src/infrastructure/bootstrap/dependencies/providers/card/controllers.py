from dishka import Provider, Scope, provide

from domain.entities.card import Card
from domain.interfaces import CMDUseCase, DataController, NonePresenter, ResultPresenter
from domain.interfaces.card import CardQueryService
from domain.use_cases.card.commands import (
    ChooseCardCommand,
    CreateCardCommand,
    DeleteAllCardsCommand,
    DeleteCardCommand,
    UpdateCardCommand,
    UpdateCardMetaCommand,
)
from domain.use_cases.card.types import CardsCountType
from infrastructure.database.query_services.card.projections import (
    CardsInfoCollectionProjection,
)
from interface_adapters.controllers.card import (
    AddCard,
    DeleteAllCards,
    DeleteCard,
    GetCardsInfo,
    SelectOneCard,
    UpdateCard,
    UpdateCardTitle,
)
from interface_adapters.controllers.card.schemas import (
    AddCardSchema,
    DeleteAllCardsSchema,
    DeleteCardSchema,
    GetCardsInfoSchema,
    SelectOneCardSchema,
    UpdateCardSchema,
    UpdateCardTitleSchema,
)
from interface_adapters.presenters.views import MapView


class CardControllerProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_add_card(
            self,
            use_case: CMDUseCase[CreateCardCommand, Card],
            presenter: ResultPresenter[Card, MapView]
    ) -> DataController[AddCardSchema, MapView]:
        return AddCard(use_case, presenter)

    @provide
    def provide_delete_all_cards(
            self,
            use_case: CMDUseCase[DeleteAllCardsCommand, CardsCountType],
            presenter: ResultPresenter[CardsCountType, MapView]
    ) -> DataController[DeleteAllCardsSchema, MapView]:
        return DeleteAllCards(use_case, presenter)

    @provide
    def provide_delete_card(
            self,
            use_case: CMDUseCase[DeleteCardCommand, None],
            presenter: NonePresenter[MapView]
    ) -> DataController[DeleteCardSchema, MapView]:
        return DeleteCard(use_case, presenter)

    @provide
    def provide_get_cards_info(
            self,
            query_service: CardQueryService[CardsInfoCollectionProjection],
            presenter: ResultPresenter[CardsInfoCollectionProjection, MapView]
    ) -> DataController[GetCardsInfoSchema, MapView]:
        return GetCardsInfo(query_service, presenter)

    @provide
    def provide_select_one_card(
            self,
            use_case: CMDUseCase[ChooseCardCommand, Card],
            presenter: ResultPresenter[Card, MapView]
    ) -> DataController[SelectOneCardSchema, MapView]:
        return SelectOneCard(use_case, presenter)

    @provide
    def provide_update_card(
            self,
            use_case: CMDUseCase[UpdateCardCommand, Card],
            presenter: ResultPresenter[Card, MapView]
    ) -> DataController[UpdateCardSchema, MapView]:
        return UpdateCard(use_case, presenter)

    @provide
    def provide_update_card_title(
            self,
            use_case: CMDUseCase[UpdateCardMetaCommand, Card],
            presenter: ResultPresenter[Card, MapView]
    ) -> DataController[UpdateCardTitleSchema, MapView]:
        return UpdateCardTitle(use_case, presenter)

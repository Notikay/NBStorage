from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session

from domain.interfaces.card import CardQueryService
from infrastructure.database.query_services.card import CardProvider
from infrastructure.database.query_services.card.projections import (
    CardsInfoCollectionProjection,
)


class CardQueryServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_card_provider(
            self,
            session: Session
    ) -> CardQueryService[CardsInfoCollectionProjection]:
        return CardProvider(session)

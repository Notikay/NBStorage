from dishka import Provider, Scope, provide

from domain.entities.card import Card
from domain.interfaces import CMDUseCase
from domain.interfaces.card import CardUnitOfWork
from domain.use_cases.card import (
    ChooseCard,
    CreateCard,
    DeleteAllCards,
    DeleteCard,
    UpdateCard,
    UpdateCardMeta,
)
from domain.use_cases.card.commands import (
    ChooseCardCommand,
    CreateCardCommand,
    DeleteAllCardsCommand,
    DeleteCardCommand,
    UpdateCardCommand,
    UpdateCardMetaCommand,
)
from domain.use_cases.card.types import CardsCountType


class CardUseCaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_choose_card(
            self,
            uow: CardUnitOfWork
    ) -> CMDUseCase[ChooseCardCommand, Card]:
        return ChooseCard(uow)

    @provide
    def provide_create_card(
            self,
            uow: CardUnitOfWork
    ) -> CMDUseCase[CreateCardCommand, Card]:
        return CreateCard(uow)

    @provide
    def provide_delete_card(
            self,
            uow: CardUnitOfWork
    ) -> CMDUseCase[DeleteCardCommand, None]:
        return DeleteCard(uow)

    @provide
    def provide_delete_all_cards(
            self,
            uow: CardUnitOfWork
    ) -> CMDUseCase[DeleteAllCardsCommand, CardsCountType]:
        return DeleteAllCards(uow)

    @provide
    def provide_update_card(
            self,
            uow: CardUnitOfWork
    ) -> CMDUseCase[UpdateCardCommand, Card]:
        return UpdateCard(uow)

    @provide
    def provide_update_card_meta(
            self,
            uow: CardUnitOfWork
    ) -> CMDUseCase[UpdateCardMetaCommand, Card]:
        return UpdateCardMeta(uow)

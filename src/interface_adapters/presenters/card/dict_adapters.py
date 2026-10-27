from collections.abc import Sequence
from typing import TypedDict

from domain.entities.card import Card, CardMeta
from domain.interfaces import ObjectStore
from domain.use_cases.card.types import CardsCountType
from infrastructure.database.query_services.card.projections import (
    CardInfoProjection,
    CardsInfoCollectionProjection,
)

from ..mixins import ShowErrorMapMixin
from ..views import MapView

type CardIDResultType = str
type CardTitleResultType = str
type CardIconURLResultType = str
type CardParamResultType = str | None


class CardMetaDict(TypedDict):
    card_id: CardIDResultType
    user_id: str
    title: CardTitleResultType
    icon_url: CardIconURLResultType


class CardDict(TypedDict):
    meta: CardMetaDict
    username: CardParamResultType
    email: CardParamResultType
    password: CardParamResultType
    url: CardParamResultType
    description: CardParamResultType


class CardInfoDict(TypedDict):
    card_id: CardIDResultType
    title: CardTitleResultType
    icon_url: CardIconURLResultType


class CardDictAdapter(ShowErrorMapMixin):
    """Адаптер карточки пользователя в словарь."""

    def __init__(self, object_store: ObjectStore) -> None:
        self.__object_store = object_store

    def show_success(self, result: Card | Sequence[Card]) -> MapView:
        if isinstance(result, Sequence):
            result_list_dict = list(map(self.__convert_card_to_dict, result))
            return MapView(
                "Перечень карточек пользователя успешно получен!",
                result_list_dict
            )

        result_dict = self.__convert_card_to_dict(result)
        return MapView("Карточка пользователя успешно получена!", result_dict)

    def __convert_card_to_dict(self, card: Card) -> CardDict:
        card_id = str(card.meta.card_id)
        user_id = str(card.meta.user_id)
        icon_url = self.__object_store.get_url(card.meta.icon_key, private=True) \
            if card.meta.icon_key \
            else self.__object_store.get_url(card.meta.get_default_icon_key())

        username = card.username.decode('utf-8') if card.username is not None else None
        email = card.email.decode('utf-8') if card.email is not None else None
        password = card.password.decode('utf-8') if card.password is not None else None
        url = card.url.decode('utf-8') if card.url is not None else None
        description = card.description.decode('utf-8')\
            if card.description is not None else None

        return {
            'meta': {
                'card_id': card_id,
                'user_id': user_id,
                'title': card.meta.title,
                'icon_url': icon_url
            },
            'username': username,
            'email': email,
            'password': password,
            'url': url,
            'description': description
        }


class CardsCountDictAdapter(ShowErrorMapMixin):
    """Адаптер количества карточек пользователя в словарь."""

    def show_success(self, result: CardsCountType) -> MapView:
        result_dict = {'cards_count': result}
        return MapView(
            "Количество карточек пользователя успешно получено!",
            result_dict
        )


class CardsInfoDictAdapter(ShowErrorMapMixin):
    """Адаптер информации о карточках пользователя в словарь."""

    def __init__(self, object_store: ObjectStore) -> None:
        self.__object_store = object_store

    def show_success(
            self,
            result: CardsInfoCollectionProjection
    ) -> MapView:
        user_id = str(result.user_id)
        cards_info = list(map(self.__convert_card_info_to_dict, result.cards_info))
        result_dict = {
            'user_id': user_id,
            'cards_info': cards_info
        }
        return MapView(
            "Перечень информации о карточках пользователя успешно получен!",
            result_dict
        )

    def __convert_card_info_to_dict(
            self,
            card_info: CardInfoProjection
    ) -> CardInfoDict:
        card_id = str(card_info.card_id)
        icon_url = self.__object_store.get_url(card_info.icon_key, private=True) \
            if card_info.icon_key \
            else self.__object_store.get_url(CardMeta.get_default_icon_key())

        return {
            'card_id': card_id,
            'title': card_info.title,
            'icon_url': icon_url
        }

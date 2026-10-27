from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from domain.interfaces import DataController
from interface_adapters.controllers.card.schemas import (
    DeleteCardSchema,
    SelectOneCardSchema,
    UpdateCardSchema,
    UpdateCardTitleSchema,
)
from interface_adapters.presenters.views import MapView

from ..schemas.card import (
    CardResponseSchema,
    UpdateCardRequestSchema,
    UpdateCardTitleRequestSchema,
)

router = APIRouter(
    prefix="/cards",
    tags=["Cards"],
)


@router.get(
    "/{card_id}",
    response_model=CardResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получение карточки пользователя",
)
@inject
def get_card(
        card_id: UUID,
        controller: FromDishka[DataController[SelectOneCardSchema, MapView]]
) -> CardResponseSchema:
    result = controller(
        SelectOneCardSchema(card_id=card_id)
    )
    return CardResponseSchema.model_validate(result.result)


@router.patch(
    "/{card_id}",
    response_model=CardResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновление карточки пользователя",
)
@inject
def update_card(
        card_id: UUID,
        data: UpdateCardRequestSchema,
        controller: FromDishka[DataController[UpdateCardSchema, MapView]]
) -> CardResponseSchema:
    result = controller(
        UpdateCardSchema(
            **{'card_id': card_id} | data.model_dump()
        )
    )
    return CardResponseSchema.model_validate(result.result)


@router.put(
    "/{card_id}/title",
    response_model=CardResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновление заголовка карточки пользователя",
)
@inject
def update_card_title(
        card_id: UUID,
        data: UpdateCardTitleRequestSchema,
        controller: FromDishka[DataController[UpdateCardTitleSchema, MapView]]
) -> CardResponseSchema:
    result = controller(
        UpdateCardTitleSchema(
            **{'card_id': card_id} | data.model_dump()
        )
    )
    return CardResponseSchema.model_validate(result.result)


@router.delete(
    "/{card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление карточки пользователя",
)
@inject
def delete_card(
        card_id: UUID,
        controller: FromDishka[DataController[DeleteCardSchema, MapView]]
) -> None:
    controller(
        DeleteCardSchema(card_id=card_id)
    )

# TODO: Загрузка логотипа карточки пользователя
# TODO: Генерация пароля

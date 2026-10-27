from typing import Annotated
from uuid import UUID

from dishka import FromComponent
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status

from domain.interfaces import DataController, NoneController
from interface_adapters.controllers.card.schemas import (
    AddCardSchema,
    DeleteAllCardsSchema,
    GetCardsInfoSchema,
)
from interface_adapters.controllers.user.schemas import (
    SelectOneUserSchema,
    DeleteUserSchema,
    UpdateUserSchema,
    UpdateUserSettingsSchema,
)
from interface_adapters.controllers.user.schemas import RegistrationUserSchema
from interface_adapters.presenters.views import MapView

from ..schemas.card import (
    AddCardRequestSchema,
    CardResponseSchema,
    CardsInfoResponseSchema,
    DeletedCardsCountResponseSchema,
)
from ..schemas.user import (
    RegistrationUserRequestSchema,
    UpdateUserRequestSchema,
    UpdateUserSettingsRequestSchema,
    UserResponseSchema,
    UsersInfoResponseSchema,
    DeletedUsersCountResponseSchema,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/{user_id}/cards",
    response_model=CardsInfoResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получение информации о всех карточках пользователя"
)
@inject
def get_cards_info(
        user_id: UUID,
        controller: FromDishka[DataController[GetCardsInfoSchema, MapView]]
) -> CardsInfoResponseSchema:
    result = controller(
        GetCardsInfoSchema(user_id=user_id)
    )
    return CardsInfoResponseSchema.model_validate(result.result)


@router.delete(
    "/{user_id}/cards",
    response_model=DeletedCardsCountResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Удаление всех карточек пользователя",
)
@inject
def delete_all_cards(
        user_id: UUID,
        controller: FromDishka[DataController[DeleteAllCardsSchema, MapView]]
) -> DeletedCardsCountResponseSchema:
    result = controller(
        DeleteAllCardsSchema(user_id=user_id)
    )
    return DeletedCardsCountResponseSchema.model_validate(result.result)


@router.post(
    "/{user_id}/cards",
    response_model=CardResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание карточки пользователя",
)
@inject
def create_card(
        user_id: UUID,
        data: AddCardRequestSchema,
        controller: FromDishka[DataController[AddCardSchema, MapView]]
) -> CardResponseSchema:
    result = controller(
        AddCardSchema(
            **{'user_id': user_id} | data.model_dump()
        )
    )
    return CardResponseSchema.model_validate(result.result)


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание пользователя",
)
@inject
def create_user(
        data: RegistrationUserRequestSchema,
        controller: FromDishka[DataController[RegistrationUserSchema, MapView]]
) -> UserResponseSchema:
    result = controller(data)
    return UserResponseSchema.model_validate(result.result)


@router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получение пользователя",
)
@inject
def get_user(
        user_id: UUID,
        controller: FromDishka[DataController[SelectOneUserSchema, MapView]]
) -> UserResponseSchema:
    result = controller(
        SelectOneUserSchema(user_id=user_id)
    )
    return UserResponseSchema.model_validate(result.result)


@router.get(
    "/",
    response_model=UsersInfoResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получение информации о всех пользователях",
)
@inject
def get_users_info(
        controller: FromDishka[Annotated[
            NoneController[MapView],
            FromComponent('get_users_info')
        ]]
) -> UsersInfoResponseSchema:
    result = controller()
    return UsersInfoResponseSchema.model_validate(result.result)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление пользователя",
)
@inject
def delete_user(
        user_id: UUID,
        controller: FromDishka[DataController[DeleteUserSchema, MapView]]
) -> None:
    controller(
        DeleteUserSchema(user_id=user_id)
    )


@router.delete(
    "/",
    response_model=DeletedUsersCountResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Удаление всех пользователей",
)
@inject
def delete_all_users(
        controller: FromDishka[Annotated[
            NoneController[MapView],
            FromComponent('delete_all_users')
        ]]
) -> DeletedUsersCountResponseSchema:
    result = controller()
    return DeletedUsersCountResponseSchema.model_validate(result.result)


@router.patch(
    "/{user_id}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновление пользователя",
)
@inject
def update_user(
        user_id: UUID,
        data: UpdateUserRequestSchema,
        controller: FromDishka[DataController[UpdateUserSchema, MapView]]
) -> UserResponseSchema:
    result = controller(
        UpdateUserSchema(
            **{'user_id': user_id} | data.model_dump()
        )
    )
    return UserResponseSchema.model_validate(result.result)


# @router.patch(
#     "/{user_id}",
#     response_model=UserResponseSchema,
#     status_code=status.HTTP_200_OK,
#     summary="Обновление настроек пользователя",
# )
# @inject
# def update_user_settings(
#         user_id: UUID,
#         data: UpdateUserSettingsRequestSchema,
#         controller: FromDishka[DataController[UpdateUserSettingsSchema, MapView]]
# ) -> UserResponseSchema:
#     result = controller(
#         UpdateUserSettingsSchema(
#             **{'user_id': user_id} | data.model_dump()
#         )
#     )
#     return UserResponseSchema.model_validate(result.result)


# TODO: Сделать отдельные роуты/контроллеры на name, time_block и загрузку аватара
# TODO: JWT

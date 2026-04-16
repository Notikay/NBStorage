from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces.units.card.exceptions import CardUseCaseError

if TYPE_CHECKING:
    from domain.interfaces.units.card.card_types import (
        MetaDataUserLoginType,
        MetaDataCardIDType
    )


class CardNotFoundError(CardUseCaseError):
    """
    Ошибка при поиске карточки пользователя.

    :ivar user_login: Атрибут логина пользователя.
    :type user_login: MetaDataUserLoginType

    :ivar card_id: Атрибут ID карточки пользователя.
    :type card_id: MetaDataCardIDType
    """

    def __init__(
            self,
            user_login: MetaDataUserLoginType,
            card_id: MetaDataCardIDType
    ):
        """
        Инициализация ошибки.

        :param user_login: Логин пользователя.
        :type user_login: MetaDataUserLoginType

        :param card_id: ID карточки пользователя.
        :type card_id: MetaDataCardIDType
        """
        self.user_login = user_login
        self.card_id = card_id

    @override
    @property
    def message(self) -> str:
        return ("Карточка пользователя не найдена! -> "
                f"{self.card_id} ({self.user_login})")

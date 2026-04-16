from __future__ import annotations

from typing import TYPE_CHECKING, override

from domain.interfaces.units.card.exceptions import CardRepositoryError

if TYPE_CHECKING:
    from domain.interfaces.units.card.card_types import (
        MetaDataUserLoginType,
        MetaDataCardIDType
    )


class CardCreateError(CardRepositoryError):
    """
    Ошибка создания карточки пользователя в хранилище.

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
        return ("Ошибка создания карточки пользователя в хранилище! -> "
                f"{self.card_id} ({self.user_login})")


class CardDeleteError(CardRepositoryError):
    """
    Ошибка удаления карточки пользователя из хранилища.

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
        return ("Ошибка удаления карточки пользователя из хранилища! -> "
                f"{self.card_id} ({self.user_login})")


class CardDeleteAllError(CardRepositoryError):
    """
    Ошибка удаления всех карточек пользователя из хранилища.

    :ivar user_login: Атрибут логина пользователя.
    :type user_login: MetaDataUserLoginType
    """

    def __init__(self, user_login: MetaDataUserLoginType):
        """
        Инициализация ошибки.

        :param user_login: Логин пользователя.
        :type user_login: MetaDataUserLoginType
        """
        self.user_login = user_login

    @override
    @property
    def message(self) -> str:
        return ("Ошибка удаления всех карточек пользователя из хранилища! -> "
                f"{self.user_login}")

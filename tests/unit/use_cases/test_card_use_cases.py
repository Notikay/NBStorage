from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from domain.use_cases import (
    ChooseCard,
    ChooseAllCards,
    CreateCard,
    DeleteCard,
    DeleteAllCards,
    UpdateCard,
    UpdateMetaData
)
from domain.entities import Card
from domain.use_cases.card.exceptions import CardNotFoundError

if TYPE_CHECKING:
    from pytest_mock import MockType


class TestCard:
    """Тестирование бизнес-логики карточки пользователя."""

    METADATA_TEST_PARAMS = (
        'test_title',
        Path('./data/icon.png'),
        'test_user_login'
    )
    UPD_METADATA_TEST_PARAMS = ('test_new_title', None)

    CARD_TEST_PARAMS = ('test_param'.encode('utf-8'),)*5
    UPD_CARD_TEST_PARAMS = (
        'test_new_param'.encode('utf-8'),
        None,
        'test_new_param'.encode('utf-8'),
        None,
        'test_new_param'.encode('utf-8')
    )

    @pytest.fixture
    def all_cards(self, card: Card, another_card: Card) -> list[Card]:
        return [card, another_card]

    # === Позитивные тесты ===
    def test_create_choose_card(self, mock_card_uow: MockType):
        assert ChooseCard(mock_card_uow), \
            "Ошибка при создании бизнес-логики выбора карточки пользователя!"

    def test_create_choose_all_cards(self, mock_card_uow: MockType):
        assert ChooseAllCards(mock_card_uow), (
            "Ошибка при создании бизнес-логики выбора всех карточек "
            "пользователя!"
        )

    def test_create_create_card(self, mock_card_uow: MockType):
        assert CreateCard(mock_card_uow), \
            "Ошибка при создании бизнес-логики создания карточки пользователя!"

    def test_create_delete_card(self, mock_card_uow: MockType):
        assert DeleteCard(mock_card_uow), \
            "Ошибка при создании бизнес-логики удаления карточки пользователя!"

    def test_create_delete_all_cards(self, mock_card_uow: MockType):
        assert DeleteAllCards(mock_card_uow), (
            "Ошибка при создании бизнес-логики удаления всех карточек "
            "пользователя!"
        )

    def test_create_update_card(self, mock_card_uow: MockType):
        assert UpdateCard(mock_card_uow), (
            "Ошибка при создании бизнес-логики обновления карточки "
            "пользователя!"
        )

    def test_create_update_metadata(self, mock_card_uow: MockType):
        assert UpdateMetaData(mock_card_uow), (
            "Ошибка при создании бизнес-логики обновления метаданных карточки "
            "пользователя!"
        )

    def test_choose_card_successfully_already_exists(
            self,
            mock_card_uow: MockType,
            card: Card
    ):
        user_login = self.METADATA_TEST_PARAMS[2]
        card_id = card.metadata.card_id

        choose_card = ChooseCard(mock_card_uow)
        result = choose_card.execute(user_login, card_id)

        assert result.metadata.user_login == user_login, \
            "Неверный логин пользователя в карточке!"
        assert result.metadata.card_id == card_id, \
            "Неверный ID карточки пользователя!"

        mock_card_uow.card_repos.get_item.assert_called_once_with(
            user_login,
            card_id
        )

    def test_choose_all_cards_successfully_already_exists(
            self,
            mock_card_uow: MockType,
            all_cards: list[Card]
    ):
        user_login = self.METADATA_TEST_PARAMS[2]

        choose_all_cards = ChooseAllCards(mock_card_uow)
        result = choose_all_cards.execute(user_login)

        assert len(result) == len(all_cards), \
            "Неверное количество карточек пользователя!"
        for i, res in enumerate(result):
            res_login = res.metadata.user_login
            res_card_id = res.metadata.card_id
            assert res_login == all_cards[i].metadata.user_login, \
                f"Неверный логин пользователя в {i+1} карточке!"
            assert res_card_id == all_cards[i].metadata.card_id, \
                f"Неверный ID в {i+1} карточке пользователя!"

        mock_card_uow.card_repos.get_all_items.assert_called_once_with(
            user_login
        )

    def test_choose_all_cards_successfully_not_existed(
            self,
            mock_card_uow: MockType
    ):
        user_login = self.METADATA_TEST_PARAMS[2]

        mock_card_uow.card_repos.get_all_items.return_value = []

        choose_all_cards = ChooseAllCards(mock_card_uow)
        result = choose_all_cards.execute(user_login)

        assert len(result) == 0, "У пользователя не должно быть карточек!"

        mock_card_uow.card_repos.get_all_items.assert_called_once_with(
            user_login
        )

    def test_create_card_successfully(self, mock_card_uow: MockType):
        title, icon_path, user_login = self.METADATA_TEST_PARAMS
        username, email, password, url, description = self.CARD_TEST_PARAMS

        create_card = CreateCard(mock_card_uow)
        result = create_card.execute(
            user_login,
            title,
            icon_path,
            username,
            email,
            password,
            url,
            description
        )

        assert result.metadata.title == title, \
            "Неверное название карточки пользователя!"
        assert result.metadata.icon_path == icon_path, \
            "Неверный путь к иконке карточки пользователя!"
        assert result.metadata.user_login == user_login, \
            "Неверный логин в карточке пользователя!"
        assert result.username == username, \
            "Неверное имя пользователя от сервиса в карточке пользователя!"
        assert result.email == email, \
            "Неверная электронная почта от сервиса в карточке пользователя!"
        assert result.password == password, \
            "Неверный пароль от сервиса в карточке пользователя!"
        assert result.url == url, \
            "Неверный URL-адрес на сервис в карточке пользователя!"
        assert result.description == description, \
            "Неверное описание сервиса в карточке пользователя!"

        mock_card_uow.card_repos.set_item.assert_called_once()

    def test_delete_card_successfully(
            self,
            mock_card_uow: MockType,
            card: Card
    ):
        user_login = self.METADATA_TEST_PARAMS[2]
        card_id = card.metadata.card_id

        delete_card = DeleteCard(mock_card_uow)
        delete_card.execute(user_login, card_id)

        mock_card_uow.card_repos.del_item.assert_called_once_with(
            user_login,
            card_id
        )

    def test_delete_all_cards_successfully(self, mock_card_uow: MockType):
        user_login = self.METADATA_TEST_PARAMS[2]

        delete_all_cards = DeleteAllCards(mock_card_uow)
        delete_all_cards.execute(user_login)

        mock_card_uow.card_repos.del_all_items.assert_called_once_with(
            user_login
        )

    def test_update_card_successfully_already_exists(
            self,
            mock_card_uow: MockType,
            card: Card
    ):
        user_login = self.METADATA_TEST_PARAMS[2]
        card_id = card.metadata.card_id

        username, email, password, url, description = self.UPD_CARD_TEST_PARAMS

        update_card = UpdateCard(mock_card_uow)
        result = update_card.execute(
            user_login,
            card_id,
            username,
            email,
            password,
            url,
            description
        )

        assert result.metadata.user_login == user_login, \
            "Неверный логин в карточке пользователя!"
        assert result.metadata.card_id == card_id, \
            "Неверный ID карточки пользователя!"

        if username is None:
            assert result.username == card.username, (
                "Имя пользователя от сервиса, в карточке пользователя не "
                "должно быть изменено!"
            )
        else:
            assert result.username == username, \
                "Неверное имя пользователя от сервиса в карточке пользователя!"

        if email is None:
            assert result.email == card.email, (
                "Электронная почта от сервиса, в карточке пользователя не "
                "должна быть изменена!"
            )
        else:
            assert result.email == email, (
                "Неверная электронная почта от сервиса в карточке "
                "пользователя!"
            )

        if password is None:
            assert result.password == card.password, (
                "Пароль от сервиса, в карточке пользователя не должен быть "
                "изменен!"
            )
        else:
            assert result.password == password, \
                "Неверный пароль от сервиса в карточке пользователя!"

        if url is None:
            assert result.url == card.url, (
                "URL-адрес на сервис, в карточке пользователя не должен быть "
                "изменен!"
            )
        else:
            assert result.url == url, \
                "Неверный URL-адрес на сервис в карточке пользователя!"

        if description is None:
            assert result.description == card.description, (
                "Описание сервиса, в карточке пользователя не должно быть "
                "изменено!"
            )
        else:
            assert result.description == description, \
                "Неверное описание сервиса в карточке пользователя!"

        mock_card_uow.card_repos.get_item.assert_called_once_with(
            user_login,
            card_id
        )
        mock_card_uow.card_repos.upd_item.assert_called_once()

    def test_update_metadata_successfully_already_exists(
            self,
            mock_card_uow: MockType,
            card: Card
    ):
        user_login, card_id = card.metadata.user_login, card.metadata.card_id
        title, icon_path = self.UPD_METADATA_TEST_PARAMS

        update_metadata = UpdateMetaData(mock_card_uow)
        result = update_metadata.execute(user_login, card_id, title, icon_path)

        assert result.metadata.user_login == user_login, \
            "Неверный логин в карточке пользователя!"
        assert result.metadata.card_id == card_id, \
            "Неверный ID карточки пользователя!"

        if title is None:
            assert result.metadata.title == card.metadata.title, \
                "Название карточки пользователя не должно быть изменено!"
        else:
            assert result.metadata.title == title, \
                "Неверное название карточки пользователя!"

        if icon_path is None:
            assert result.metadata.icon_path == card.metadata.icon_path, \
                "Путь к иконке карточки пользователя не должен быть изменен!"
        else:
            assert result.metadata.icon_path == icon_path, \
                "Неверный путь к иконке карточки пользователя!"

        mock_card_uow.card_repos.get_item.assert_called_once_with(
            user_login,
            card_id
        )
        mock_card_uow.card_repos.upd_item.assert_called_once()

    # === Негативные тесты ===
    def test_choose_card_raises_not_found_not_existed(
            self,
            mock_card_uow: MockType,
            card: Card
    ):
        user_login = self.METADATA_TEST_PARAMS[2]
        card_id = card.metadata.card_id

        mock_card_uow.card_repos.get_item.return_value = None

        choose_card = ChooseCard(mock_card_uow)
        with pytest.raises(CardNotFoundError):
            choose_card.execute(user_login, card_id)

    def test_update_card_raises_not_found_not_existed_for_get_item(
            self,
            mock_card_uow: MockType,
            card: Card,
    ):
        user_login = self.METADATA_TEST_PARAMS[2]
        card_id = card.metadata.card_id

        mock_card_uow.card_repos.get_item.return_value = None

        update_card = UpdateCard(mock_card_uow)
        with pytest.raises(CardNotFoundError):
            update_card.execute(
                user_login,
                card_id,
                *self.UPD_CARD_TEST_PARAMS
            )

    def test_update_card_raises_not_found_not_existed_for_upd_item(
            self,
            mock_card_uow: MockType,
            card: Card,
    ):
        user_login = self.METADATA_TEST_PARAMS[2]
        card_id = card.metadata.card_id

        mock_card_uow.card_repos.upd_item.return_value = None

        update_card = UpdateCard(mock_card_uow)
        with pytest.raises(CardNotFoundError):
            update_card.execute(
                user_login,
                card_id,
                *self.UPD_CARD_TEST_PARAMS
            )

    def test_update_metadata_raises_not_found_not_existed_for_get_item(
            self,
            mock_card_uow: MockType,
            card: Card,
    ):
        user_login = self.METADATA_TEST_PARAMS[2]
        card_id = card.metadata.card_id

        mock_card_uow.card_repos.get_item.return_value = None

        update_metadata = UpdateMetaData(mock_card_uow)
        with pytest.raises(CardNotFoundError):
            update_metadata.execute(
                user_login,
                card_id,
                *self.UPD_METADATA_TEST_PARAMS
            )

    def test_update_metadata_raises_not_found_not_existed_for_upd_item(
            self,
            mock_card_uow: MockType,
            card: Card,
    ):
        user_login = self.METADATA_TEST_PARAMS[2]
        card_id = card.metadata.card_id

        mock_card_uow.card_repos.upd_item.return_value = None

        update_metadata = UpdateMetaData(mock_card_uow)
        with pytest.raises(CardNotFoundError):
            update_metadata.execute(
                user_login,
                card_id,
                *self.UPD_METADATA_TEST_PARAMS
            )

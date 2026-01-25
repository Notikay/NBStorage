from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from domain.entities import MetaData, Card

if TYPE_CHECKING:
    from domain.entities import MetaDataDTO, CardDTO


class TestMetaData:
    """Тестирование метаданных карточки пользователя."""

    METADATA_TEST_PARAMS = (
        'test_title',
        Path('./data/icon.png'),
        'test_user_login'
    )

    @pytest.fixture
    def meta_dict(self, meta: MetaData) -> MetaDataDTO:
        return meta.to_dict()

    # === Позитивные тесты ===
    def test_create_metadata(self):
        meta = MetaData(*self.METADATA_TEST_PARAMS)
        assert meta, "Ошибка при создании метаданных карточки пользователя!"

    def test_return_metadata_correct_values(self, meta: MetaData):
        assert meta.title == self.METADATA_TEST_PARAMS[0], \
            "Название карточки пользователя не совпадает с входным!"
        assert meta.icon_path == self.METADATA_TEST_PARAMS[1], \
            "Путь к иконке карточки пользователя не совпадает с входным!"
        assert meta.user_login == self.METADATA_TEST_PARAMS[2], (
            "Логин пользователя, которому принадлежит карточка, не совпадает "
            "с входным!"
        )

    def test_return_metadata_key_is_not_empty(self, meta: MetaData):
        assert meta.key, "Ключ в метаданных карточки пользователя пуст!"

    def test_return_metadata_key_is_unique(self, meta: MetaData):
        another_key = MetaData(*self.METADATA_TEST_PARAMS).key
        assert another_key != meta.key, \
            "Ключ в метаданных карточки пользователя не уникален!"

    def test_return_metadata_card_id_is_not_empty(self, meta: MetaData):
        assert meta.card_id, "ID карточки пользователя пуст!"

    def test_return_metadata_card_id_is_unique(self, meta: MetaData):
        another_card_id = MetaData(*self.METADATA_TEST_PARAMS).card_id
        assert another_card_id != meta.card_id, \
            "ID карточки пользователя не уникален!"

    def test_return_metadata_to_dict_is_dict_type(
            self,
            meta_dict: MetaDataDTO
    ):
        assert isinstance(meta_dict, dict), \
            "Ошибка преобразования метаданных карточки пользователя в словарь!"

    def test_return_metadata_to_dict_is_not_empty(
            self,
            meta_dict: MetaDataDTO
    ):
        assert meta_dict, "Словарь метаданных карточки пользователя пуст!"

    def test_return_metadata_to_dict_icon_path_is_str_type(
            self,
            meta_dict: MetaDataDTO
    ):
        assert isinstance(meta_dict['icon_path'], str), \
            "Путь к иконке карточки пользователя не является строкой!"

    def test_return_metadata_to_dict_card_id_is_str_type(
            self,
            meta_dict: MetaDataDTO
    ):
        assert isinstance(meta_dict['card_id'], str), \
            "ID карточки пользователя не является строкой!"

    def test_successful_metadata_to_dict_correct_values(
            self,
            meta: MetaData,
            meta_dict: MetaDataDTO
    ):
        assert meta_dict['title'] == meta.title, (
            "Название карточки пользователя, из словаря метаданных, не "
            "совпадает с названием из экземпляра класса!"
        )
        assert meta_dict['icon_path'] == str(meta.icon_path), (
            "Путь к иконке карточки пользователя, из словаря метаданных, не "
            "совпадает с путем из экземпляра класса!"
        )
        assert meta_dict['user_login'] == meta.user_login, (
            "Логин пользователя, которому принадлежит карточка, из словаря "
            "метаданных, не совпадает с логином из экземпляра класса!"
        )
        assert meta_dict['card_id'] == str(meta.card_id), (
            "ID карточки пользователя, из словаря метаданных, не совпадает с "
            "ID из экземпляра класса!"
        )

    # === Негативные тесты ===
    def test_raises_value_error_metadata_when_title_is_empty(self):
        with pytest.raises(ValueError):
            MetaData('', Path('./icon.png'), 'test_user_login')

    def test_raises_value_error_metadata_when_icon_path_incorrect_ext(self):
        with pytest.raises(ValueError):
            MetaData('test_title', Path('./icon.bad_ext'), 'test_user_login')

    def test_raises_value_error_metadata_when_icon_path_is_empty(self):
        with pytest.raises(ValueError):
            MetaData('test_title', Path(''), 'test_user_login')

    def test_raises_value_error_metadata_when_user_login_is_empty(self):
        with pytest.raises(ValueError):
            MetaData('test_title', Path('./icon.png'), '')


class TestCard:
    """Тестирование карточки пользователя."""

    METADATA_TEST_PARAMS = (
        'test_title',
        Path('./data/icon.png'),
        'test_user_login'
    )
    CARD_TEST_PARAMS = ('test_param'.encode('utf-8'),)*5

    @pytest.fixture
    def card(self, meta: MetaData) -> Card:
        return Card(meta, *self.CARD_TEST_PARAMS)

    @pytest.fixture
    def card_none(self, meta: MetaData) -> Card:
        return Card(meta, None, None, None, None, None)

    @pytest.fixture
    def card_dict(self, card: Card) -> CardDTO:
        return card.to_dict()

    # === Позитивные тесты ===
    def test_create_card(self, meta: MetaData):
        assert Card(meta, *self.CARD_TEST_PARAMS), \
            "Ошибка при создании карточки пользователя!"

    def test_return_card_correct_values(self, card: Card):
        assert card.username == self.CARD_TEST_PARAMS[0], (
            "Имя пользователя от сервиса, в карточке пользователя, не "
            "совпадает с входным!"
        )
        assert card.email == self.CARD_TEST_PARAMS[1], (
            "Электронная почта от сервиса, в карточке пользователя, не "
            "совпадает с входным!"
        )
        assert card.password == self.CARD_TEST_PARAMS[2], (
            "Пароль от сервиса, в карточке пользователя, не совпадает с "
            "входным!"
        )
        assert card.url == self.CARD_TEST_PARAMS[3], (
            "URL-адрес от сервиса, в карточке пользователя, не совпадает с "
            "входным!"
        )
        assert card.description == self.CARD_TEST_PARAMS[4], (
            "Описание сервиса, в карточке пользователя, не совпадает с "
            "входным!"
        )

    def test_return_card_to_dict_is_dict_type(self, card_dict: CardDTO):
        assert isinstance(card_dict, dict), \
            "Ошибка преобразования карточки пользователя в словарь!"

    def test_return_card_to_dict_is_not_empty(self, card_dict: CardDTO):
        assert card_dict, "Словарь карточки пользователя пуст!"

    def test_successful_card_to_dict_correct_meta(
            self,
            card: Card,
            card_dict: CardDTO
    ):
        assert card_dict['meta'] == card.meta.to_dict(), (
            "Метаданные карточки пользователя, из словаря карточки "
            "пользователя, не совпадают с метаданными из экземпляра класса!"
        )

    def test_successful_card_to_dict_correct_values(
            self,
            card: Card,
            card_dict: CardDTO
    ):
        assert card.username is not None, (
            "Имя пользователя от сервиса, в карточке пользователя, является "
            "None!"
        )
        assert card.email is not None, (
            "Электронная почта от сервиса, в карточке пользователя, является "
            "None!"
        )
        assert card.password is not None, \
            "Пароль от сервиса, в карточке пользователя, является None!"
        assert card.url is not None, \
            "URL-адрес от сервиса, в карточке пользователя, является None!"
        assert card.description is not None, \
            "Описание сервиса, в карточке пользователя, является None!"

        assert card_dict['username'] == card.username.decode('utf-8'), (
            "Имя пользователя от сервиса, из словаря карточки пользователя, "
            "не совпадает с именем пользователя от сервиса из экземпляра "
            "класса!"
        )
        assert card_dict['email'] == card.email.decode('utf-8'), (
            "Электронная почта от сервиса, из словаря карточки пользователя, "
            "не совпадает с электронной почтой от сервиса из экземпляра "
            "класса!"
        )
        assert card_dict['password'] == card.password.decode('utf-8'), (
            "Пароль от сервиса, из словаря карточки пользователя, не "
            "совпадает с паролем от сервиса из экземпляра класса!"
        )
        assert card_dict['url'] == card.url.decode('utf-8'), (
            "URL-адрес от сервиса, из словаря карточки пользователя, не "
            "совпадает с URL-адресом от сервиса из экземпляра класса!"
        )
        assert card_dict['description'] == card.description.decode('utf-8'), (
            "Описание сервиса, из словаря карточки пользователя, не совпадает "
            "с описанием сервиса из экземпляра класса!"
        )

    def test_successful_card_to_dict_correct_none(self, card_none: Card):
        card_dict = card_none.to_dict()
        assert card_dict['username'] is None, (
            "Имя пользователя от сервиса, из словаря карточки пользователя, "
            "не является None!"
        )
        assert card_dict['email'] is None, (
            "Электронная почта от сервиса, из словаря карточки пользователя, "
            "не является None!"
        )
        assert card_dict['password'] is None, (
            "Пароль от сервиса, из словаря карточки пользователя, не является "
            "None!"
        )
        assert card_dict['url'] is None, (
            "URL-адрес от сервиса, из словаря карточки пользователя, не "
            "является None!"
        )
        assert card_dict['description'] is None, (
            "Описание сервиса, из словаря карточки пользователя, не является "
            "None!"
        )

    def test_return_card_encrypt_change_params(self, card: Card):
        card.encrypt()
        assert card.username != self.CARD_TEST_PARAMS[0], (
            "Имя пользователя от сервиса, в карточке пользователя, не было "
            "зашифровано!"
        )
        assert card.email != self.CARD_TEST_PARAMS[1], (
            "Электронная почта от сервиса, в карточке пользователя, не была "
            "зашифрована!"
        )
        assert card.password != self.CARD_TEST_PARAMS[2], \
            "Пароль от сервиса, в карточке пользователя, не был зашифрован!"
        assert card.url != self.CARD_TEST_PARAMS[3], \
            "URL-адрес от сервиса, в карточке пользователя, не был зашифрован!"
        assert card.description != self.CARD_TEST_PARAMS[4], \
            "Описание сервиса, в карточке пользователя, не было зашифровано!"

    def test_return_card_encrypt_not_change_none_params(self, card_none: Card):
        card_none.encrypt()
        assert card_none.username is None, (
            "Имя пользователя от сервиса, в карточке пользователя, не "
            "является None!"
        )
        assert card_none.email is None, (
            "Электронная почта от сервиса, в карточке пользователя, не "
            "является None!"
        )
        assert card_none.password is None, \
            "Пароль от сервиса, в карточке пользователя, не является None!"
        assert card_none.url is None, \
            "URL-адрес от сервиса, в карточке пользователя, не является None!"
        assert card_none.description is None, \
            "Описание сервиса, в карточке пользователя, не является None!"

    def test_return_card_decrypt_change_params(self, card: Card):
        card.decrypt()
        assert card.username != self.CARD_TEST_PARAMS[0], (
            "Имя пользователя от сервиса, в карточке пользователя, не было "
            "расшифровано!"
        )
        assert card.email != self.CARD_TEST_PARAMS[1], (
            "Электронная почта от сервиса, в карточке пользователя, не была "
            "расшифрована!"
        )
        assert card.password != self.CARD_TEST_PARAMS[2], \
            "Пароль от сервиса, в карточке пользователя, не был расшифрован!"
        assert card.url != self.CARD_TEST_PARAMS[3], (
            "URL-адрес от сервиса, в карточке пользователя, не был "
            "расшифрован!"
        )
        assert card.description != self.CARD_TEST_PARAMS[4], \
            "Описание сервиса, в карточке пользователя, не было расшифровано!"

    def test_return_card_decrypt_not_change_none_params(self, card_none):
        card_none.decrypt()
        assert card_none.username is None, (
            "Имя пользователя от сервиса, в карточке пользователя, не "
            "является None!"
        )
        assert card_none.email is None, (
            "Электронная почта от сервиса, в карточке пользователя, не "
            "является None!"
        )
        assert card_none.password is None, \
            "Пароль от сервиса, в карточке пользователя, не является None!"
        assert card_none.url is None, \
            "URL-адрес от сервиса, в карточке пользователя, не является None!"
        assert card_none.description is None, \
            "Описание сервиса, в карточке пользователя, не является None!"

    def test_successful_card_encrypt_decrypt_pipeline(self, card: Card):
        card.encrypt()
        card.decrypt()
        assert card.username == self.CARD_TEST_PARAMS[0], (
            "Результат шифровки и расшифровки имени пользователя от сервиса "
            "прошел некорректно!"
        )
        assert card.email == self.CARD_TEST_PARAMS[1], (
            "Результат шифровки и расшифровки электронной почты от сервиса "
            "прошел некорректно!"
        )
        assert card.password == self.CARD_TEST_PARAMS[2], (
            "Результат шифровки и расшифровки пароля от сервиса прошел "
            "некорректно!"
        )
        assert card.url == self.CARD_TEST_PARAMS[3], (
            "Результат шифровки и расшифровки URL-адреса от сервиса прошел "
            "некорректно!"
        )
        assert card.description == self.CARD_TEST_PARAMS[4], (
            "Результат шифровки и расшифровки описания сервиса прошел "
            "некорректно!"
        )

    def test_successful_card_encrypt_decrypt_pipeline_for_several_cards(
            self,
            card: Card
    ):
        another_meta = MetaData(*self.METADATA_TEST_PARAMS)
        another_card = Card(another_meta, *self.CARD_TEST_PARAMS)

        card.encrypt()
        another_card.encrypt()

        assert another_card.username != card.username, (
            "Результат шифровки имени пользователя от сервиса, для разных "
            "карточек пользователей, одинаков!"
        )
        assert another_card.email != card.email, (
            "Результат шифровки электронной почты от сервиса, для разных "
            "карточек пользователей, одинаков!"
        )
        assert another_card.password != card.password, (
            "Результат шифровки пароля от сервиса, для разных карточек "
            "пользователей, одинаков!"
        )
        assert another_card.url != card.url, (
            "Результат шифровки URL-адреса от сервиса, для разных карточек "
            "пользователей, одинаков!"
        )
        assert another_card.description != card.description, (
            "Результат шифровки описания сервиса, для разных карточек "
            "пользователей, одинаков!"
        )

        card.decrypt()
        another_card.decrypt()

        assert another_card.username == card.username, (
            "Результат расшифровки имени пользователя от сервиса, для разных "
            "карточек пользователей с одинаковыми данными, разный!"
        )
        assert another_card.email == card.email, (
            "Результат расшифровки электронной почты от сервиса, для разных "
            "карточек пользователей с одинаковыми данными, разный!"
        )
        assert another_card.password == card.password, (
            "Результат расшифровки пароля от сервиса, для разных карточек "
            "пользователей с одинаковыми данными, разный!"
        )
        assert another_card.url == card.url, (
            "Результат расшифровки URL-адреса от сервиса, для разных карточек "
            "пользователей с одинаковыми данными, разный!"
        )
        assert another_card.description == card.description, (
            "Результат расшифровки описания сервиса, для разных карточек "
            "пользователей с одинаковыми данными, разный!"
        )

    def test_successful_card_check_is_encrypted_flag(self, card: Card):
        card.encrypt()
        assert card.is_encrypted, (
            "Флаг шифровки показывает, что данные карточки пользователя не "
            "зашифрованы!"
        )
        card.decrypt()
        assert not card.is_encrypted, (
            "Флаг шифровки показывает, что данные карточки пользователя "
            "зашифрованы!"
        )

    def test_return_card_xor_otp_encrypt_is_none(self, card: Card):
        encrypted_param = card.xor_otp_encrypt(None, card.meta.key)
        assert encrypted_param is None, \
            "Результат шифровки None, не является None!"

    def test_successful_card_xor_otp_encrypt(self, card: Card):
        encrypted_param = card.xor_otp_encrypt(
            self.CARD_TEST_PARAMS[0],
            card.meta.key
        )
        assert encrypted_param != self.CARD_TEST_PARAMS[0], \
            "Результат шифровки параметра не отличается от исходного!"
        decrypt_param = card.xor_otp_encrypt(encrypted_param, card.meta.key)
        assert decrypt_param == self.CARD_TEST_PARAMS[0], \
            "Результат расшифровки параметра не совпадает с исходным!"

    # === Негативные тесты ===
    def test_raises_value_error_card_when_param_is_equal_key(
            self,
            meta: MetaData
    ):
        with pytest.raises(ValueError):
            Card(meta, meta.key, None, None, None, None)

    def test_raises_value_error_card_when_param_is_empty(self, meta: MetaData):
        with pytest.raises(ValueError):
            Card(meta, b'', None, None, None, None)

    def test_raises_value_error_card_when_key_start_with_param(
            self,
            meta: MetaData
    ):
        test_param = meta.key[:5]
        with pytest.raises(ValueError):
            Card(meta, test_param, None, None, None, None)

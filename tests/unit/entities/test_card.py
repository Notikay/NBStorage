from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from domain.entities import MetaData

if TYPE_CHECKING:
    from domain.entities import MetaDataDTO


class TestMetaData:
    """Тестирование метаданных карточки пользователя."""

    METADATA_TEST_PARAMS = (
        'test_title',
        Path('./data/icon.png'),
        'test_user_login'
    )

    @pytest.fixture
    def meta(self) -> MetaData:
        return MetaData(*self.METADATA_TEST_PARAMS)

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
            "Название карточки пользователя из словаря метаданных не "
            "совпадает с названием из экземпляра класса!"
        )
        assert meta_dict['icon_path'] == str(meta.icon_path), (
            "Путь к иконке карточки пользователя из словаря метаданных не "
            "совпадает с путем из экземпляра класса!"
        )
        assert meta_dict['user_login'] == meta.user_login, (
            "Логин пользователя, которому принадлежит карточка, из словаря "
            "метаданных не совпадает с логином из экземпляра класса!"
        )
        assert meta_dict['card_id'] == str(meta.card_id), (
            "ID карточки пользователя из словаря метаданных не совпадает с "
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

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from domain.entities import Settings

if TYPE_CHECKING:
    from domain.entities import SettingsDTO


class TestSettings:
    """Тестирование настроек пользователя."""

    SETTINGS_TEST_PARAMS = (
        'test_name',
        Path('./data/avatar.png'),
        60
    )

    @pytest.fixture
    def settings_dict(self, settings: Settings) -> SettingsDTO:
        return settings.to_dict()

    # === Позитивные тесты ===
    def test_create_settings(self):
        settings = Settings(*self.SETTINGS_TEST_PARAMS)
        assert settings, "Ошибка при создании настроек пользователя!"

    def test_return_settings_correct_values(self, settings: Settings):
        assert settings.name == self.SETTINGS_TEST_PARAMS[0], \
            "Имя пользователя не совпадает с входным!"
        assert settings.avatar_path == self.SETTINGS_TEST_PARAMS[1], \
            "Путь к аватарке пользователя не совпадает с входным!"
        assert settings.time_block == self.SETTINGS_TEST_PARAMS[2], \
            "Время блокировки сессии пользователя не совпадает с входным!"

    def test_return_settings_to_dict_is_dict_type(
            self,
            settings_dict: SettingsDTO
    ):
        assert isinstance(settings_dict, dict), \
            "Ошибка преобразования настроек пользователя в словарь!"

    def test_return_settings_to_dict_is_not_empty(
            self,
            settings_dict: SettingsDTO
    ):
        assert settings_dict, "Словарь настроек пользователя пуст!"

    def test_return_settings_to_dict_avatar_path_is_str_type(
            self,
            settings_dict: SettingsDTO
    ):
        assert isinstance(settings_dict['avatar_path'], str), \
            "Путь к аватарке пользователя не является строкой!"

    def test_successful_settings_to_dict_correct_values(
            self,
            settings: Settings,
            settings_dict: SettingsDTO
    ):
        assert settings_dict['name'] == settings.name, (
            "Имя пользователя, из словаря настроек, не совпадает с именем из "
            "экземпляра класса!"
        )
        assert settings_dict['avatar_path'] == str(settings.avatar_path), (
            "Путь к аватарке пользователя, из словаря настроек, не совпадает "
            "с путем из экземпляра класса!"
        )
        assert settings_dict['time_block'] == settings.time_block, (
            "Время блокировки сессии пользователя, из словаря настроек, не "
            "совпадает с временем из экземпляра класса!"
        )

    # === Негативные тесты ===
    def test_raises_value_error_settings_when_name_is_empty(self):
        with pytest.raises(ValueError):
            Settings('', Path('./avatar.png'), 60)

    def test_raises_value_error_settings_when_avatar_path_incorrect_ext(self):
        with pytest.raises(ValueError):
            Settings('test_name', Path('./avatar.bad_ext'), 60)

    def test_raises_value_error_settings_when_avatar_path_is_empty(self):
        with pytest.raises(ValueError):
            Settings('test_name', Path(''), 60)

    def test_raises_value_error_settings_when_time_block_is_negative(self):
        with pytest.raises(ValueError):
            Settings('test_name', Path('./avatar.png'), -1)

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from domain.entities import Settings, User

if TYPE_CHECKING:
    from domain.entities import SettingsDTO, UserDTO


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


class TestUser:
    """Тестирование пользователя."""

    SETTINGS_TEST_PARAMS = (
        'test_name',
        Path('./data/avatar.png'),
        60
    )
    USER_TEST_PARAMS = ('test_login', 'test_password'.encode('utf-8'))

    @pytest.fixture
    def user(self, settings: Settings) -> User:
        return User(settings, *self.USER_TEST_PARAMS)

    @pytest.fixture
    def user_dict(self, user: User) -> UserDTO:
        return user.to_dict()

    # === Позитивные тесты ===
    def test_create_user(self, settings: Settings):
        assert User(settings, *self.USER_TEST_PARAMS), \
            "Ошибка при создании пользователя!"

    def test_return_user_correct_values(self, user: User):
        assert user.login == self.USER_TEST_PARAMS[0], \
            "Логин пользователя не совпадает с входным!"
        assert user.password == self.USER_TEST_PARAMS[1], \
            "Пароль пользователя не совпадает с входным!"

    def test_return_user_salt_is_not_empty(self, user: User):
        assert user.salt, "Соль, для хеширования пароля пользователя, пуста!"

    def test_return_user_salt_is_unique(self, settings: Settings, user: User):
        another_salt = User(settings, *self.USER_TEST_PARAMS).salt
        assert another_salt != user.salt, \
            "Соль, для хеширования пароля пользователя, не уникальна!"

    def test_return_user_to_dict_is_dict_type(self, user_dict: UserDTO):
        assert isinstance(user_dict, dict), \
            "Ошибка преобразования пользователя в словарь!"

    def test_return_user_to_dict_is_not_empty(self, user_dict: UserDTO):
        assert user_dict, "Словарь пользователя пуст!"

    def test_successful_user_to_dict_correct_values(
            self,
            user: User,
            user_dict: UserDTO
    ):
        assert user_dict['settings'] == user.settings.to_dict(), (
            "Настройки пользователя, из словаря пользователя, не совпадают "
            "с настройками из экземпляра класса!"
        )
        assert user_dict['login'] == user.login, (
            "Логин пользователя, из словаря пользователя, не совпадает с "
            "логином из экземпляра класса!"
        )

    def test_return_user_hash_password_change_password(self, user: User):
        user.hash_password()
        assert user.password != self.USER_TEST_PARAMS[1], \
            "Пароль пользователя не был хеширован!"

    def test_return_user_sha15_hash_password(self, user: User):
        hash_password = user.sha512_hash_password(
            self.USER_TEST_PARAMS[1],
            user.salt
        )
        assert hash_password != self.USER_TEST_PARAMS[1], \
            "Пароль не был хеширован!"

    # === Негативные тесты ===
    def test_raises_value_error_user_when_login_is_empty(
            self,
            settings: Settings
    ):
        with pytest.raises(ValueError):
            User(settings, '', self.USER_TEST_PARAMS[1])

    def test_raises_value_error_user_when_password_is_empty(
            self,
            settings: Settings
    ):
        with pytest.raises(ValueError):
            User(settings, self.USER_TEST_PARAMS[0], b'')

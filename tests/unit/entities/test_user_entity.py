from pathlib import Path

import pytest

from domain.entities import Settings, User
from domain.entities.user.exceptions import (
    SettingsInvalidNameError,
    SettingsInvalidAvatarPathError,
    SettingsInvalidTimeBlockError,
    UserInvalidLoginError,
    UserInvalidPasswordError
)


class TestSettings:
    """Тестирование настроек пользователя."""

    SETTINGS_TEST_PARAMS = (
        'test_name',
        Path('./data/avatar.png'),
        60
    )

    # === Позитивные тесты ===
    def test_create_settings(self):
        assert Settings(*self.SETTINGS_TEST_PARAMS), \
            "Ошибка при создании настроек пользователя!"

    def test_settings_return_correct_values(self):
        settings = Settings(*self.SETTINGS_TEST_PARAMS)

        assert settings.name == self.SETTINGS_TEST_PARAMS[0], \
            "Имя пользователя не совпадает с входным!"
        assert settings.avatar_path == self.SETTINGS_TEST_PARAMS[1], \
            "Путь к аватарке пользователя не совпадает с входным!"
        assert settings.time_block == self.SETTINGS_TEST_PARAMS[2], \
            "Время блокировки сессии пользователя не совпадает с входным!"

    def test_settings_return_to_dict_is_dict_type(self):
        settings_dict = Settings(*self.SETTINGS_TEST_PARAMS).to_dict()

        assert isinstance(settings_dict, dict), \
            "Ошибка преобразования настроек пользователя в словарь!"

    def test_settings_return_to_dict_is_not_empty(self):
        settings_dict = Settings(*self.SETTINGS_TEST_PARAMS).to_dict()

        assert settings_dict, "Словарь настроек пользователя пуст!"

    def test_settings_return_to_dict_avatar_path_is_str_type(self):
        settings_dict = Settings(*self.SETTINGS_TEST_PARAMS).to_dict()

        assert isinstance(settings_dict['avatar_path'], str), \
            "Путь к аватарке пользователя не является строкой!"

    def test_settings_successful_to_dict_correct_values(self):
        settings = Settings(*self.SETTINGS_TEST_PARAMS)
        settings_dict = settings.to_dict()

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
    def test_settings_raises_invalid_name_is_empty(self):
        with pytest.raises(SettingsInvalidNameError):
            Settings('', Path('./avatar.png'), 60)

    def test_settings_raises_invalid_avatar_path_incorrect_ext(self):
        with pytest.raises(SettingsInvalidAvatarPathError):
            Settings('test_name', Path('./avatar.bad_ext'), 60)

    def test_settings_raises_invalid_avatar_path_is_empty(self):
        with pytest.raises(SettingsInvalidAvatarPathError):
            Settings('test_name', Path(''), 60)

    def test_settings_raises_invalid_time_block_is_negative(self):
        with pytest.raises(SettingsInvalidTimeBlockError):
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
    def settings(self) -> Settings:
        return Settings(*self.SETTINGS_TEST_PARAMS)

    # === Позитивные тесты ===
    def test_create_user(self, settings: Settings):
        assert User(settings, *self.USER_TEST_PARAMS), \
            "Ошибка при создании пользователя!"

    def test_user_return_correct_values(self, settings: Settings):
        user = User(settings, *self.USER_TEST_PARAMS)

        assert user.login == self.USER_TEST_PARAMS[0], \
            "Логин пользователя не совпадает с входным!"
        assert user.password == self.USER_TEST_PARAMS[1], \
            "Пароль пользователя не совпадает с входным!"

    def test_user_return_salt_is_not_empty(self, settings: Settings):
        salt = User(settings, *self.USER_TEST_PARAMS).salt

        assert salt, "Соль, для хеширования пароля пользователя, пуста!"

    def test_user_return_salt_is_unique(self, settings: Settings):
        salt = User(settings, *self.USER_TEST_PARAMS).salt
        another_salt = User(settings, *self.USER_TEST_PARAMS).salt

        assert another_salt != salt, \
            "Соль, для хеширования пароля пользователя, не уникальна!"

    def test_user_return_to_dict_is_dict_type(self, settings: Settings):
        user_dict = User(settings, *self.USER_TEST_PARAMS).to_dict()

        assert isinstance(user_dict, dict), \
            "Ошибка преобразования пользователя в словарь!"

    def test_user_return_to_dict_is_not_empty(self, settings: Settings):
        user_dict = User(settings, *self.USER_TEST_PARAMS).to_dict()

        assert user_dict, "Словарь пользователя пуст!"

    def test_user_successful_to_dict_correct_values(self, settings: Settings):
        user = User(settings, *self.USER_TEST_PARAMS)
        user_dict = user.to_dict()

        assert user_dict['settings'] == user.settings.to_dict(), (
            "Настройки пользователя, из словаря пользователя, не совпадают "
            "с настройками из экземпляра класса!"
        )
        assert user_dict['login'] == user.login, (
            "Логин пользователя, из словаря пользователя, не совпадает с "
            "логином из экземпляра класса!"
        )

    def test_user_return_hash_password_change_password(
            self,
            settings: Settings
    ):
        user = User(settings, *self.USER_TEST_PARAMS)
        user.hash_password()

        assert user.password != self.USER_TEST_PARAMS[1], \
            "Пароль пользователя не был хеширован!"

    def test_user_return_sha15_hash_password(self, settings: Settings):
        user = User(settings, *self.USER_TEST_PARAMS)
        hash_password = user.sha512_hash_password(
            self.USER_TEST_PARAMS[1],
            user.salt
        )

        assert hash_password != self.USER_TEST_PARAMS[1], \
            "Пароль не был хеширован!"

    # === Негативные тесты ===
    def test_user_raises_invalid_login_is_empty(self, settings: Settings):
        with pytest.raises(UserInvalidLoginError):
            User(settings, '', self.USER_TEST_PARAMS[1])

    def test_user_raises_invalid_password_is_empty(self, settings: Settings):
        with pytest.raises(UserInvalidPasswordError):
            User(settings, self.USER_TEST_PARAMS[0], b'')

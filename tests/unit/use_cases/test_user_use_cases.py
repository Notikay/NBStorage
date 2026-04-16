from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from domain.use_cases import (
    ChooseUser,
    ChooseAllUsers,
    CreateUser,
    DeleteUser,
    DeleteAllUsers,
    UpdateSettings,
    ChangeUserPassword
)
from domain.entities import User
from domain.use_cases.user.exceptions import UserNotFoundError

if TYPE_CHECKING:
    from pytest_mock import MockType


class TestUser:
    """Тестирование бизнес-логики пользователя."""

    SETTINGS_TEST_PARAMS = (
        'test_name',
        Path('./data/avatar.png'),
        60
    )
    UPD_SETTINGS_TEST_PARAMS = ('test_new_name', None, 60)

    USER_TEST_PARAMS = ('test_login', 'test_password'.encode('utf-8'))
    UPD_USER_TEST_PARAMS = ('test_new_password'.encode('utf-8'),)

    @pytest.fixture
    def all_users(self, user: User, another_user: User) -> list[User]:
        return [user, another_user]

    # === Позитивные тесты ===
    def test_create_choose_user(self, mock_user_uow: MockType):
        assert ChooseUser(mock_user_uow), \
            "Ошибка при создании бизнес-логики выбора пользователя!"

    def test_create_choose_all_users(self, mock_user_uow: MockType):
        assert ChooseAllUsers(mock_user_uow), \
            "Ошибка при создании бизнес-логики получения всех пользователей!"

    def test_create_create_user(self, mock_user_uow: MockType):
        assert CreateUser(mock_user_uow), \
            "Ошибка при создании бизнес-логики создания пользователя!"

    def test_create_delete_user(self, mock_user_uow: MockType):
        assert DeleteUser(mock_user_uow), \
            "Ошибка при создании бизнес-логики удаления пользователя!"

    def test_create_delete_all_users(self, mock_user_uow: MockType):
        assert DeleteAllUsers(mock_user_uow), \
            "Ошибка при создании бизнес-логики удаления всех пользователей!"

    def test_create_update_settings(self, mock_user_uow: MockType):
        assert UpdateSettings(mock_user_uow), (
            "Ошибка при создании бизнес-логики обновления настроек "
            "пользователя!"
        )

    def test_create_change_user_password(self, mock_user_uow: MockType):
        assert ChangeUserPassword(mock_user_uow), \
            "Ошибка при создании бизнес-логики изменения пароля пользователя!"

    def test_choose_user_successfully_already_exists(
            self,
            mock_user_uow: MockType
    ):
        login = self.USER_TEST_PARAMS[0]

        choose_user = ChooseUser(mock_user_uow)
        result = choose_user.execute(login)

        assert result.login == login, "Неверный логин пользователя!"

        mock_user_uow.user_repos.get_item.assert_called_once_with(login)

    def test_choose_all_users_successfully_already_exists(
            self,
            mock_user_uow: MockType,
            all_users: list[User]
    ):
        choose_all_users = ChooseAllUsers(mock_user_uow)
        result = choose_all_users.execute()

        for i, res in enumerate(result):
            assert res.login == all_users[i].login, \
                f"Неверный логин у {i+1}-го пользователя!"

        mock_user_uow.user_repos.get_all_items.assert_called_once_with()

    def test_choose_all_users_successfully_not_existed(
            self,
            mock_user_uow: MockType
    ):
        mock_user_uow.user_repos.get_all_items.return_value = []

        choose_all_users = ChooseAllUsers(mock_user_uow)
        result = choose_all_users.execute()

        assert len(result) == 0, "Не должно быть пользователей!"

        mock_user_uow.user_repos.get_all_items.assert_called_once_with()

    def test_create_user_successfully_already_exists(
            self,
            mock_user_uow: MockType
    ):
        login, password = self.USER_TEST_PARAMS
        name, avatar_path, time_block = self.SETTINGS_TEST_PARAMS

        create_user = CreateUser(mock_user_uow)
        result = create_user.execute(
            login,
            password,
            name,
            avatar_path,
            time_block
        )

        assert result.login == login, "Неверный логин пользователя!"
        assert result.password != password, "Пароль пользователя не хеширован!"
        assert result.settings.name == name, "Неверное имя пользователя!"
        assert result.settings.avatar_path == avatar_path, \
            "Неверный путь к аватарке пользователя!"
        assert result.settings.time_block == time_block, \
            "Неверное время блокировки сессии пользователя!"

        mock_user_uow.user_repos.set_item.assert_called_once()

    def test_delete_user_successfully_already_exists(
            self,
            mock_user_uow: MockType
    ):
        login = self.USER_TEST_PARAMS[0]

        delete_user = DeleteUser(mock_user_uow)
        delete_user.execute(login)

        mock_user_uow.user_repos.del_item.assert_called_once_with(login)

    def test_delete_all_users_successfully_already_exists(
            self,
            mock_user_uow: MockType
    ):
        delete_all_users = DeleteAllUsers(mock_user_uow)
        delete_all_users.execute()

        mock_user_uow.user_repos.del_all_items.assert_called_once_with()

    def test_update_settings_successfully_already_exists(
            self,
            mock_user_uow: MockType,
            user: User
    ):
        login = self.USER_TEST_PARAMS[0]
        name, avatar_path, time_block = self.UPD_SETTINGS_TEST_PARAMS

        update_settings = UpdateSettings(mock_user_uow)
        result = update_settings.execute(login, name, avatar_path, time_block)

        assert result.login == login, "Неверный логин пользователя!"

        if name is None:
            assert result.settings.name == user.settings.name, \
                "Имя пользователя не должно быть изменено!"
        else:
            assert result.settings.name == name, \
                "Неверное имя пользователя!"

        if avatar_path is None:
            assert result.settings.avatar_path == user.settings.avatar_path, \
                "Путь к аватарке пользователя не должен быть изменен!"
        else:
            assert result.settings.avatar_path == avatar_path, \
                "Неверный путь к аватарке пользователя!"

        if time_block is None:
            assert result.settings.time_block == user.settings.time_block, \
                "Время блокировки сессии пользователя не должно быть изменено!"
        else:
            assert result.settings.time_block == time_block, \
                "Неверное время блокировки сессии пользователя!"

        mock_user_uow.user_repos.get_item.assert_called_once_with(login)
        mock_user_uow.user_repos.upd_item.assert_called_once()

    def test_change_user_password_successfully_already_exists(
            self,
            mock_user_uow: MockType
    ):
        login = self.USER_TEST_PARAMS[0]
        password = self.UPD_USER_TEST_PARAMS[0]

        change_user_password = ChangeUserPassword(mock_user_uow)
        result = change_user_password.execute(login, password)

        assert result.login == login, "Неверный логин пользователя!"
        assert result.password != password, "Пароль пользователя не хеширован!"

        mock_user_uow.user_repos.get_item.assert_called_once_with(login)
        mock_user_uow.user_repos.upd_item.assert_called_once()

    # === Негативные тесты ===
    def test_choose_user_raises_not_found_not_existed(
            self,
            mock_user_uow: MockType,
            user: User
    ):
        login = self.USER_TEST_PARAMS[0]

        mock_user_uow.user_repos.get_item.return_value = None

        choose_user = ChooseUser(mock_user_uow)
        with pytest.raises(UserNotFoundError):
            choose_user.execute(login)

    def test_update_settings_raises_not_found_not_existed_for_get_item(
            self,
            mock_user_uow: MockType,
            user: User,
    ):
        login = self.USER_TEST_PARAMS[0]

        mock_user_uow.user_repos.get_item.return_value = None

        update_settings = UpdateSettings(mock_user_uow)
        with pytest.raises(UserNotFoundError):
            update_settings.execute(login, *self.UPD_SETTINGS_TEST_PARAMS)

    def test_update_settings_raises_not_found_not_existed_for_upd_item(
            self,
            mock_user_uow: MockType,
            user: User,
    ):
        login = self.USER_TEST_PARAMS[0]

        mock_user_uow.user_repos.upd_item.return_value = None

        update_settings = UpdateSettings(mock_user_uow)
        with pytest.raises(UserNotFoundError):
            update_settings.execute(login, *self.UPD_SETTINGS_TEST_PARAMS)

    def test_change_password_raises_not_found_not_existed_for_get_item(
            self,
            mock_user_uow: MockType,
            user: User,
    ):
        login = self.USER_TEST_PARAMS[0]

        mock_user_uow.user_repos.get_item.return_value = None

        change_user_password = ChangeUserPassword(mock_user_uow)
        with pytest.raises(UserNotFoundError):
            change_user_password.execute(login, *self.UPD_USER_TEST_PARAMS)

    def test_change_password_raises_not_found_not_existed_for_upd_item(
            self,
            mock_user_uow: MockType,
            user: User,
    ):
        login = self.USER_TEST_PARAMS[0]

        mock_user_uow.user_repos.upd_item.return_value = None

        change_user_password = ChangeUserPassword(mock_user_uow)
        with pytest.raises(UserNotFoundError):
            change_user_password.execute(login, *self.UPD_USER_TEST_PARAMS)

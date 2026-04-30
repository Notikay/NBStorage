from collections import namedtuple
from pathlib import Path

import pytest

from domain.entities import UserMeta, User
from domain.entities.user.exceptions import (
    UserMetaInvalidNameError,
    UserMetaInvalidAvatarPathError,
    UserMetaInvalidTimeBlockError,
    UserInvalidLoginError,
    UserInvalidPasswordError
)


MetaTestParams = namedtuple(
    'MetaTestParams',
    ('name', 'avatar_path', 'time_block')
)
UserTestParams = namedtuple('UserTestParams', ('login', 'password'))

META_TEST_PARAMS = MetaTestParams('test_name', Path('./data/avatar.png'), 60)
USER_TEST_PARAMS = UserTestParams(
    'test_login',
    'test_password'.encode('utf-8')
)


@pytest.fixture
def meta() -> UserMeta:
    return UserMeta(*META_TEST_PARAMS)

# === Позитивные тесты метаданных пользователя ===
def test_create_meta():
    assert UserMeta(*META_TEST_PARAMS), \
        "Ошибка при создании метаданных пользователя!"

def test_meta_return_correct_values():
    meta = UserMeta(*META_TEST_PARAMS)

    assert meta.name == META_TEST_PARAMS.name, \
        "Имя пользователя не совпадает с входным!"
    assert meta.avatar_path == META_TEST_PARAMS.avatar_path, \
        "Путь к аватарке пользователя не совпадает с входным!"
    assert meta.time_block == META_TEST_PARAMS.time_block, \
        "Время блокировки сессии пользователя не совпадает с входным!"

def test_meta_return_salt_is_not_empty():
    salt = UserMeta(*META_TEST_PARAMS).salt

    assert salt, "Соль хеширования пароля пользователя, пуста!"

def test_meta_return_salt_is_unique():
    salt = UserMeta(*META_TEST_PARAMS).salt
    another_salt = UserMeta(*META_TEST_PARAMS).salt

    assert another_salt != salt, \
        "Соль хеширования пароля пользователя, не уникальна!"

def test_meta_return_to_dict_is_dict_type():
    meta_dict = UserMeta(*META_TEST_PARAMS).to_dict()

    assert isinstance(meta_dict, dict), \
        "Ошибка преобразования метаданных пользователя в словарь!"

def test_meta_return_to_dict_is_not_empty():
    meta_dict = UserMeta(*META_TEST_PARAMS).to_dict()

    assert meta_dict, "Словарь метаданных пользователя пуст!"

def test_meta_return_to_dict_avatar_path_is_str_type():
    meta_dict = UserMeta(*META_TEST_PARAMS).to_dict()

    assert isinstance(meta_dict['avatar_path'], str), \
        "Путь к аватарке пользователя не является строкой!"

def test_meta_successful_to_dict_correct_values():
    meta = UserMeta(*META_TEST_PARAMS)
    meta_dict = meta.to_dict()

    assert meta_dict['name'] == meta.name, (
        "Имя пользователя, из словаря метаданных, не совпадает с именем из "
        "экземпляра класса!"
    )
    assert meta_dict['avatar_path'] == str(meta.avatar_path), (
        "Путь к аватарке пользователя, из словаря метаданных, не совпадает "
        "с путем из экземпляра класса!"
    )
    assert meta_dict['time_block'] == meta.time_block, (
        "Время блокировки сессии пользователя, из словаря метаданных, не "
        "совпадает с временем из экземпляра класса!"
    )

# === Позитивные тесты пользователя ===
def test_create_user(meta: UserMeta):
    assert User(meta, *USER_TEST_PARAMS), \
        "Ошибка при создании пользователя!"

def test_user_return_correct_values(meta: UserMeta):
    user = User(meta, *USER_TEST_PARAMS)

    assert user.login == USER_TEST_PARAMS.login, \
        "Логин пользователя не совпадает с входным!"
    assert user.password == USER_TEST_PARAMS.password, \
        "Пароль пользователя не совпадает с входным!"

def test_user_return_to_dict_is_dict_type(meta: UserMeta):
    user_dict = User(meta, *USER_TEST_PARAMS).to_dict()

    assert isinstance(user_dict, dict), \
        "Ошибка преобразования пользователя в словарь!"

def test_user_return_to_dict_is_not_empty(meta: UserMeta):
    user_dict = User(meta, *USER_TEST_PARAMS).to_dict()

    assert user_dict, "Словарь пользователя пуст!"

def test_user_successful_to_dict_correct_values(meta: UserMeta):
    user = User(meta, *USER_TEST_PARAMS)
    user_dict = user.to_dict()

    assert user_dict['meta'] == user.meta.to_dict(), (
        "Метаданные пользователя, из словаря пользователя, не совпадают с "
        "метаданными из экземпляра класса!"
    )
    assert user_dict['login'] == user.login, (
        "Логин пользователя, из словаря пользователя, не совпадает с логином "
        "из экземпляра класса!"
    )

def test_user_successful_hash_password(meta: UserMeta):
    user = User(meta, *USER_TEST_PARAMS)
    user.hash_password()

    assert user.password != USER_TEST_PARAMS.password, \
        "Пароль пользователя не был хеширован!"

def test_user_successful_sha15_hash_password(meta: UserMeta):
    user = User(meta, *USER_TEST_PARAMS)
    hash_password = user.sha512_hash_password(
        USER_TEST_PARAMS.password,
        user.meta.salt
    )

    assert hash_password != USER_TEST_PARAMS[1], "Пароль не был хеширован!"

# === Негативные тесты метаданных пользователя ===
def test_meta_raises_invalid_name_is_empty():
    with pytest.raises(UserMetaInvalidNameError):
        UserMeta('', META_TEST_PARAMS.avatar_path, META_TEST_PARAMS.time_block)

def test_meta_raises_invalid_avatar_path_incorrect_ext():
    with pytest.raises(UserMetaInvalidAvatarPathError):
        UserMeta(
            META_TEST_PARAMS.name,
            Path('./avatar.bad_ext'),
            META_TEST_PARAMS.time_block
        )

def test_meta_raises_invalid_avatar_path_is_empty():
    with pytest.raises(UserMetaInvalidAvatarPathError):
        UserMeta(META_TEST_PARAMS.name, Path(''), META_TEST_PARAMS.time_block)

def test_meta_raises_invalid_time_block_is_negative():
    with pytest.raises(UserMetaInvalidTimeBlockError):
        UserMeta(META_TEST_PARAMS.name, META_TEST_PARAMS.avatar_path, -1)

# === Негативные тесты пользователя ===
def test_user_raises_invalid_login_is_empty(meta: UserMeta):
    with pytest.raises(UserInvalidLoginError):
        User(meta, '', USER_TEST_PARAMS.password)

def test_user_raises_invalid_password_is_empty(meta: UserMeta):
    with pytest.raises(UserInvalidPasswordError):
        User(meta, USER_TEST_PARAMS.login, b'')

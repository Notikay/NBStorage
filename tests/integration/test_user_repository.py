from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

import pytest

from infrastructure.persistence.models import UserORM
from infrastructure.persistence.repositories import UserStorage
from domain.entities import UserMeta, User

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class UserORMTestParams(TypedDict):
    login : str
    name: str
    avatar_path: str
    time_block: int
    password: bytes
    salt: bytes


USER_ORM_TEST_PARAMS: UserORMTestParams = {
    'login': 'test_login',
    'name': 'test_name',
    'avatar_path': 'data\\avatar.png',
    'time_block': 60,
    'password': b'\xb7AVE\x99lpjm\x0f\xf5\x14\x85\x10\x05\x91,\xf7\x8f\x98'
                b'\x9d\xce\xa58\xad_\x1b\xf0 \xa7\xe5J',
    'salt': b'0\xe2\x1c\x12j\xf0\x12\r+\x1b\xc8\xac%z(\xb4'
}

@pytest.fixture
def user_orm() -> UserORM:
    return UserORM(**USER_ORM_TEST_PARAMS)

@pytest.fixture
def user() -> User:
    user = User(
        UserMeta(
            USER_ORM_TEST_PARAMS['name'],
            Path(USER_ORM_TEST_PARAMS['avatar_path']),
            USER_ORM_TEST_PARAMS['time_block'],
            USER_ORM_TEST_PARAMS['salt']
        ),
        USER_ORM_TEST_PARAMS['login'],
        USER_ORM_TEST_PARAMS['password']
    )

    return user

# === Позитивные тесты ===
def test_create_user_storage(db_session: Session):
    assert UserStorage(db_session), \
        "Ошибка при создании хранилища пользователя!"

def test_get_item_successfully_already_exists(
        db_session: Session,
        user_orm: UserORM
):
    db_session.add(user_orm)
    db_session.flush()

    login = USER_ORM_TEST_PARAMS['login']
    name = USER_ORM_TEST_PARAMS['name']
    avatar_path = Path(USER_ORM_TEST_PARAMS['avatar_path'])
    time_block = USER_ORM_TEST_PARAMS['time_block']
    password = USER_ORM_TEST_PARAMS['password']
    salt = USER_ORM_TEST_PARAMS['salt']

    user_storage = UserStorage(db_session)
    result = user_storage.get_item(login)

    if result is None:
        pytest.fail("Пользователя нет в хранилище!")

    assert result.login == login, "Неверный логин пользователя!"
    assert result.meta.name == name, "Неверное имя пользователя!"
    assert result.meta.avatar_path == avatar_path, \
        "Неверный путь к аватарке пользователя!"
    assert result.meta.time_block == time_block, \
        "Неверное время блокировки сессии пользователя!"
    assert result.meta.salt == salt, \
        "Неверная соль хеширования пароля пользователя!"
    assert result.password == password, "Неверный хеш пароля пользователя!"

def test_get_item_successfully_not_existed(db_session: Session):
    login = USER_ORM_TEST_PARAMS['login']

    user_storage = UserStorage(db_session)
    result = user_storage.get_item(login)

    assert result is None, "Пользователь не должен существовать!"

def test_get_all_items_successfully_already_exists(
        db_session: Session,
        user_orm: UserORM
):
    another_user_orm_test_params = USER_ORM_TEST_PARAMS.copy()
    another_user_orm_test_params.update({'login': 'test_another_login'})
    another_user_orm = UserORM(**another_user_orm_test_params)

    all_users = [user_orm, another_user_orm]

    db_session.add_all(all_users)
    db_session.flush()

    user_storage = UserStorage(db_session)
    result = user_storage.get_all_items()

    assert len(result) == len(all_users), \
        "Неверное количество пользователей!"
    for num, data in enumerate(zip(result, (
            USER_ORM_TEST_PARAMS,
            another_user_orm_test_params
    )), start=1):
        res, test_params = data

        login = test_params['login']
        name = test_params['name']
        avatar_path = Path(test_params['avatar_path'])
        time_block = test_params['time_block']
        password = test_params['password']
        salt = test_params['salt']

        assert res.login == login, \
            f"Неверный логин у {num} пользователя!"
        assert res.meta.name == name, \
            f"Неверное имя у {num} пользователя!"
        assert res.meta.avatar_path == avatar_path, \
            f"Неверный путь к аватарке у {num} пользователя!"
        assert res.meta.time_block == time_block, \
            f"Неверное время блокировки сессии у {num} пользователя!"
        assert res.meta.salt == salt, \
            f"Неверная соль хеширования пароля у {num} пользователя!"
        assert res.password == password, \
            f"Неверный хеш пароля у {num} пользователя!"

def test_get_all_items_successfully_not_existed(db_session: Session):
    user_storage = UserStorage(db_session)
    result = user_storage.get_all_items()

    assert len(result) == 0, "Пользователей не должно существовать!"

def test_set_item_successfully_already_exists(
        db_session: Session,
        user_orm: UserORM,
        user: User
):
    login = USER_ORM_TEST_PARAMS['login']
    name = USER_ORM_TEST_PARAMS['name']
    avatar_path = Path(USER_ORM_TEST_PARAMS['avatar_path'])
    time_block = USER_ORM_TEST_PARAMS['time_block']
    password = USER_ORM_TEST_PARAMS['password']
    salt = USER_ORM_TEST_PARAMS['salt']

    user_storage = UserStorage(db_session)
    result = user_storage.set_item(user)

    assert result.login == login, "Неверный логин пользователя!"
    assert result.meta.name == name, "Неверное имя пользователя!"
    assert result.meta.avatar_path == avatar_path, \
        "Неверный путь к аватарке пользователя!"
    assert result.meta.time_block == time_block, \
        "Неверное время блокировки сессии пользователя!"
    assert result.meta.salt == salt, \
        "Неверная соль хеширования пароля пользователя!"
    assert result.password == password, "Неверный хеш пароля пользователя!"

def test_upd_item_successfully_already_exists(
        db_session: Session,
        user_orm: UserORM,
        user: User
):
    db_session.add(user_orm)
    db_session.flush()

    login = USER_ORM_TEST_PARAMS['login']
    avatar_path = Path(USER_ORM_TEST_PARAMS['avatar_path'])
    time_block = USER_ORM_TEST_PARAMS['time_block']
    salt = USER_ORM_TEST_PARAMS['salt']

    new_name = 'test_new_name'
    new_password = (b'~s\xfa\xce\xbf|y=m\x10\t\xe41k\x0f\xaa&\xe3U\xdc\xcd'
                    b'\xbco\xc5\x15\xd1\x84\xc5w=]F')

    user.meta.name = new_name
    user.password = new_password

    user_storage = UserStorage(db_session)
    result = user_storage.upd_item(user)

    if result is None:
        pytest.fail("Пользователя нет в хранилище")

    assert result.login == login, "Неверный логин пользователя!"
    assert result.meta.name == new_name, "Неверное имя пользователя!"
    assert result.meta.avatar_path == avatar_path, \
        "Неверный путь к аватарке пользователя!"
    assert result.meta.time_block == time_block, \
        "Неверное время блокировки сессии пользователя!"
    assert result.meta.salt == salt, \
        "Неверная соль хеширования пароля пользователя!"
    assert result.password == new_password, "Неверный хеш пароля пользователя!"

def test_upd_item_successfully_not_existed(db_session: Session, user: User):
    user_storage = UserStorage(db_session)
    result = user_storage.upd_item(user)

    assert result is None, "Пользователь не должен существовать!"

def test_del_item_successfully_already_exists(
        db_session: Session,
        user_orm: UserORM
):
    db_session.add(user_orm)
    db_session.flush()

    login = USER_ORM_TEST_PARAMS['login']

    user_storage = UserStorage(db_session)
    user_storage.del_item(login)

    db_session.flush()
    result = db_session.get(UserORM, login)

    assert result is None, "Пользователь не был удален!"

def test_del_item_successfully_not_existed(db_session: Session):
    login = USER_ORM_TEST_PARAMS['login']

    user_storage = UserStorage(db_session)
    user_storage.del_item(login)

def test_del_all_items_successfully_already_exists(
        db_session: Session,
        user_orm: UserORM
):
    another_user_orm_test_params = USER_ORM_TEST_PARAMS.copy()
    another_user_orm_test_params.update({'login': 'test_another_login'})
    another_login = another_user_orm_test_params['login']
    another_user_orm = UserORM(**another_user_orm_test_params)

    login = USER_ORM_TEST_PARAMS['login']

    all_users = [user_orm, another_user_orm]

    db_session.add_all(all_users)
    db_session.flush()

    user_storage = UserStorage(db_session)
    user_storage.del_all_items()

    db_session.flush()

    for num, login_ in enumerate((login, another_login), start=1):
        result = db_session.get(UserORM, login_)

        assert result is None, f"{num} пользователь не был удален!"

def test_del_all_items_successfully_not_existed(db_session: Session):
    user_storage = UserStorage(db_session)
    user_storage.del_all_items()

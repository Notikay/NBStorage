from __future__ import annotations

from uuid import UUID
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

import pytest

from infrastructure.persistence.models import CardORM
from infrastructure.persistence.repositories import CardStorage
from domain.entities import MetaData, Card

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class CardORMTestParams(TypedDict):
    user_login: str
    card_id: UUID
    title: str
    icon_path: str
    key: bytes
    username: bytes
    email: bytes
    password: bytes
    url: bytes
    description: bytes


CARD_ORM_TEST_PARAMS: CardORMTestParams = {
    'user_login': 'test_user_login',
    'card_id': UUID('2e35207c-3531-55a8-8ce7-abb47b2caf4f'),
    'title': 'test_title',
    'icon_path': 'data\\icon.png',
    'key': b'\xfb\xd0e\xff\x10\xa21\xe4\xb3\x1b\xf3\xe8\xf4u\xbbkh\x89\x07'
           b'\xcc"\xcc\xf4\xf0 \x9e\xf3W\x8c\xb6\xf41',
    'username': b'\x8f\xb5\x16\x8bO\xd2P\x96\xd2v',
    'email': b'\x8f\xb5\x16\x8bO\xd2P\x96\xd2v',
    'password': b'\x8f\xb5\x16\x8bO\xd2P\x96\xd2v',
    'url': b'\x8f\xb5\x16\x8bO\xd2P\x96\xd2v',
    'description': b'\x8f\xb5\x16\x8bO\xd2P\x96\xd2v'
}

@pytest.fixture
def card_orm() -> CardORM:
    return CardORM(**CARD_ORM_TEST_PARAMS)

@pytest.fixture
def card() -> Card:
    card = Card(
        MetaData(
            CARD_ORM_TEST_PARAMS['title'],
            Path(CARD_ORM_TEST_PARAMS['icon_path']),
            CARD_ORM_TEST_PARAMS['user_login'],
            CARD_ORM_TEST_PARAMS['key']
        ),
        CARD_ORM_TEST_PARAMS['username'],
        CARD_ORM_TEST_PARAMS['email'],
        CARD_ORM_TEST_PARAMS['password'],
        CARD_ORM_TEST_PARAMS['url'],
        CARD_ORM_TEST_PARAMS['description']
    )

    return card

# === Позитивные тесты ===
def test_create_card_storage(db_session: Session):
    assert CardStorage(db_session), \
        "Ошибка при создании хранилища карточек пользователя!"

def test_get_item_successfully_already_exists(
        db_session: Session,
        card_orm: CardORM
):
    db_session.add(card_orm)
    db_session.flush()

    user_login = CARD_ORM_TEST_PARAMS['user_login']
    card_id = CARD_ORM_TEST_PARAMS['card_id']
    title = CARD_ORM_TEST_PARAMS['title']
    icon_path = Path(CARD_ORM_TEST_PARAMS['icon_path'])
    key = CARD_ORM_TEST_PARAMS['key']
    username = CARD_ORM_TEST_PARAMS['username']
    email = CARD_ORM_TEST_PARAMS['email']
    password = CARD_ORM_TEST_PARAMS['password']
    url = CARD_ORM_TEST_PARAMS['url']
    description = CARD_ORM_TEST_PARAMS['description']

    card_storage = CardStorage(db_session)
    result = card_storage.get_item(user_login, card_id)

    if result is None:
        pytest.fail("Карточки пользователя нет в хранилище!")

    assert result.metadata.card_id == card_id, \
        "Неверный ID карточки пользователя!"
    assert result.metadata.user_login == user_login, \
        "Неверный логин в карточке пользователя!"
    assert result.metadata.title == title, \
        "Неверное название карточки пользователя!"
    assert result.metadata.icon_path == icon_path, \
        "Неверный путь к иконке карточки пользователя!"
    assert result.metadata.key == key, \
        "Неверный ключ шифрования для данных карточек пользователя!"
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

def test_get_item_successfully_not_existed(db_session: Session):
    user_login = CARD_ORM_TEST_PARAMS['user_login']
    card_id = CARD_ORM_TEST_PARAMS['card_id']

    card_storage = CardStorage(db_session)
    result = card_storage.get_item(user_login, card_id)

    assert result is None, "Карточка пользователя не должна существовать!"

def test_get_all_items_successfully_already_exists(
        db_session: Session,
        card_orm: CardORM
):
    another_card_orm_test_params = CARD_ORM_TEST_PARAMS.copy()
    another_card_orm_test_params.update({
        'card_id': UUID('3dde017e-f94c-59fa-9c58-4f99b53a7e4d'),
        'key': b"\x94\xbfI\x06TJ\xd4\x8f\x0b\xea\xbd+\xafO\xa2`\xe4\xc1"
               b"\x05\tW\xe0c\xbb\x84\x07\xe0\xe4\x8e9\x91'"
    })
    another_card_orm = CardORM(**another_card_orm_test_params)

    user_login = CARD_ORM_TEST_PARAMS['user_login']

    all_cards = [card_orm, another_card_orm]

    db_session.add_all(all_cards)
    db_session.flush()

    card_storage = CardStorage(db_session)
    result = card_storage.get_all_items(user_login)

    assert len(result) == len(all_cards), \
        "Неверное количество карточек пользователя!"
    for num, data in enumerate(zip(result, (
            CARD_ORM_TEST_PARAMS,
            another_card_orm_test_params
    )), start=1):
        res, test_params = data

        user_login = test_params['user_login']
        card_id = test_params['card_id']
        title = test_params['title']
        icon_path = Path(test_params['icon_path'])
        key = test_params['key']
        username = test_params['username']
        email = test_params['email']
        password = test_params['password']
        url = test_params['url']
        description = test_params['description']

        assert res.metadata.card_id == card_id, \
            f"Неверный ID в {num} карточке пользователя!"
        assert res.metadata.user_login == user_login, \
            f"Неверный логин в {num} карточке пользователя!"
        assert res.metadata.title == title, \
            f"Неверное название в {num} карточке пользователя!"
        assert res.metadata.icon_path == icon_path, \
            f"Неверный путь к иконке в {num} карточке пользователя!"
        assert res.metadata.key == key, \
            "Неверный ключ шифрования для данных карточек пользователя!"
        assert res.username == username, (
            f"Неверное имя пользователя от сервиса в {num} карточке "
            "пользователя!"
        )
        assert res.email == email, (
            f"Неверная электронная почта от сервиса в {num} карточке "
            f"пользователя!"
        )
        assert res.password == password, \
            f"Неверный пароль от сервиса в {num} карточке пользователя!"
        assert res.url == url, \
            f"Неверный URL-адрес на сервис в {num} карточке пользователя!"
        assert res.description == description, \
            f"Неверное описание сервиса в {num} карточке пользователя!"

def test_get_all_items_successfully_not_existed(db_session: Session):
    user_login = CARD_ORM_TEST_PARAMS['user_login']

    card_storage = CardStorage(db_session)
    result = card_storage.get_all_items(user_login)

    assert len(result) == 0, "У пользователя не должно быть карточек!"

def test_set_item_successfully_already_exists(
        db_session: Session,
        card_orm: CardORM,
        card: Card
):
    user_login = CARD_ORM_TEST_PARAMS['user_login']
    card_id = CARD_ORM_TEST_PARAMS['card_id']
    title = CARD_ORM_TEST_PARAMS['title']
    icon_path = Path(CARD_ORM_TEST_PARAMS['icon_path'])
    key = CARD_ORM_TEST_PARAMS['key']
    username = CARD_ORM_TEST_PARAMS['username']
    email = CARD_ORM_TEST_PARAMS['email']
    password = CARD_ORM_TEST_PARAMS['password']
    url = CARD_ORM_TEST_PARAMS['url']
    description = CARD_ORM_TEST_PARAMS['description']

    card_storage = CardStorage(db_session)
    result = card_storage.set_item(card)

    assert result.metadata.card_id == card_id, \
        "Неверный ID карточки пользователя!"
    assert result.metadata.user_login == user_login, \
        "Неверный логин в карточке пользователя!"
    assert result.metadata.title == title, \
        "Неверное название карточки пользователя!"
    assert result.metadata.icon_path == icon_path, \
        "Неверный путь к иконке карточки пользователя!"
    assert result.metadata.key == key, \
        "Неверный ключ шифрования для данных карточек пользователя!"
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

def test_upd_item_successfully_already_exists(
        db_session: Session,
        card_orm: CardORM,
        card: Card
):
    db_session.add(card_orm)
    db_session.flush()

    user_login = CARD_ORM_TEST_PARAMS['user_login']
    card_id = CARD_ORM_TEST_PARAMS['card_id']
    icon_path = Path(CARD_ORM_TEST_PARAMS['icon_path'])
    key = CARD_ORM_TEST_PARAMS['key']
    password = CARD_ORM_TEST_PARAMS['password']
    url = CARD_ORM_TEST_PARAMS['url']
    description = CARD_ORM_TEST_PARAMS['description']

    new_title = 'test_new_title'
    new_username = b'\x18\xe8\xebR8B\xb2\x9c\x9c\xaa\xb8\xc7)\x9b'
    new_email = b''

    card.metadata.title = new_title
    card.username = new_username
    card.email = new_email

    card_storage = CardStorage(db_session)
    result = card_storage.upd_item(card)

    if result is None:
        pytest.fail("Карточки пользователя нет в хранилище!")

    assert result.metadata.card_id == card_id, \
        "Неверный ID карточки пользователя!"
    assert result.metadata.user_login == user_login, \
        "Неверный логин в карточке пользователя!"
    assert result.metadata.title == new_title, \
        "Неверное название карточки пользователя!"
    assert result.metadata.icon_path == icon_path, \
        "Неверный путь к иконке карточки пользователя!"
    assert result.metadata.key == key, \
        "Неверный ключ шифрования для данных карточек пользователя!"
    assert result.username == new_username, \
        "Неверное имя пользователя от сервиса в карточке пользователя!"
    assert result.email is None, \
        "Неверная электронная почта от сервиса в карточке пользователя!"
    assert result.password == password, \
        "Неверный пароль от сервиса в карточке пользователя!"
    assert result.url == url, \
        "Неверный URL-адрес на сервис в карточке пользователя!"
    assert result.description == description, \
        "Неверное описание сервиса в карточке пользователя!"

def test_upd_item_successfully_not_existed(db_session: Session, card: Card):
    card_storage = CardStorage(db_session)
    result = card_storage.upd_item(card)

    assert result is None, "Карточка пользователя не должна существовать!"

def test_del_item_successfully_already_exists(
        db_session: Session,
        card_orm: CardORM
):
    db_session.add(card_orm)
    db_session.flush()

    user_login = CARD_ORM_TEST_PARAMS['user_login']
    card_id = CARD_ORM_TEST_PARAMS['card_id']

    card_storage = CardStorage(db_session)
    card_storage.del_item(user_login, card_id)

    db_session.flush()
    result = db_session.get(CardORM, (user_login, card_id))

    assert result is None, "Карточка пользователя не была удалена!"

def test_del_item_successfully_not_existed(db_session: Session):
    user_login = CARD_ORM_TEST_PARAMS['user_login']
    card_id = CARD_ORM_TEST_PARAMS['card_id']

    card_storage = CardStorage(db_session)
    card_storage.del_item(user_login, card_id)

def test_del_all_items_successfully_already_exists(
        db_session: Session,
        card_orm: CardORM
):
    another_card_id = UUID('3dde017e-f94c-59fa-9c58-4f99b53a7e4d')
    another_card_orm_test_params = CARD_ORM_TEST_PARAMS.copy()
    another_card_orm_test_params.update({
        'card_id': another_card_id,
        'key': b"\x94\xbfI\x06TJ\xd4\x8f\x0b\xea\xbd+\xafO\xa2`\xe4\xc1"
               b"\x05\tW\xe0c\xbb\x84\x07\xe0\xe4\x8e9\x91'"
    })
    another_card_orm = CardORM(**another_card_orm_test_params)

    user_login = CARD_ORM_TEST_PARAMS['user_login']
    card_id = CARD_ORM_TEST_PARAMS['card_id']

    all_cards = [card_orm, another_card_orm]

    db_session.add_all(all_cards)
    db_session.flush()

    card_storage = CardStorage(db_session)
    card_storage.del_all_items(user_login)

    db_session.flush()

    for num, id_ in enumerate((card_id, another_card_id), start=1):
        result = db_session.get(CardORM, (user_login, id_))

        assert result is None, \
            f"{num} карточка пользователя не была удалена!"

def test_del_all_items_successfully_not_existed(db_session: Session):
    user_login = CARD_ORM_TEST_PARAMS['user_login']

    card_storage = CardStorage(db_session)
    card_storage.del_all_items(user_login)

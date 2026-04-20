from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, TypedDict
from uuid import UUID

import pytest

from domain.entities import Card, MetaData, User, Settings
from infrastructure.persistence.models import CardORM, UserORM
from infrastructure.persistence.uow import TransactionStateManager
from infrastructure.persistence.uow.exceptions import (
    SessionIsNotInitializedError
)

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


class UserORMTestParams(TypedDict):
    login: str
    name: str
    avatar_path: str
    time_block: int
    password: bytes
    salt: bytes


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

USER_ORM_TEST_PARAMS: UserORMTestParams = {
    'login': 'test_login',
    'name': 'test_name',
    'avatar_path': 'data\\avatar.png',
    'time_block': 60,
    'password': b'\xb7AVE\x99lpjm\x0f\xf5\x14\x85\x10\x05\x91,\xf7\x8f\x98'
                b'\x9d\xce\xa58\xad_\x1b\xf0 \xa7\xe5J',
    'salt': b'0\xe2\x1c\x12j\xf0\x12\r+\x1b\xc8\xac%z(\xb4'
}


# === Позитивные тесты ===
def test_commit_successfully(db_session: Session):
    transaction_state_manager = TransactionStateManager(
        lambda: db_session  # type: ignore
    )

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

    user = User(
        Settings(
            USER_ORM_TEST_PARAMS['name'],
            Path(USER_ORM_TEST_PARAMS['avatar_path']),
            USER_ORM_TEST_PARAMS['time_block']
        ),
        USER_ORM_TEST_PARAMS['login'],
        USER_ORM_TEST_PARAMS['password'],
        USER_ORM_TEST_PARAMS['salt']
    )

    with transaction_state_manager:
        transaction_state_manager.card_repos.set_item(card)
        transaction_state_manager.user_repos.set_item(user)

        transaction_state_manager.commit()

    db_session.expunge_all()

    user_login = CARD_ORM_TEST_PARAMS['user_login']
    card_id = CARD_ORM_TEST_PARAMS['card_id']

    login = USER_ORM_TEST_PARAMS['login']

    result_card = db_session.get(CardORM, (user_login, card_id))
    result_user = db_session.get(UserORM, login)

    assert result_card is not None, "Карточки пользователя нет в хранилище!"
    assert result_user is not None, "Пользователя нет в хранилище!"


def test_rollback_successfully(db_session: Session):
    transaction_state_manager = TransactionStateManager(
        lambda: db_session  # type: ignore
    )

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

    user = User(
        Settings(
            USER_ORM_TEST_PARAMS['name'],
            Path(USER_ORM_TEST_PARAMS['avatar_path']),
            USER_ORM_TEST_PARAMS['time_block']
        ),
        USER_ORM_TEST_PARAMS['login'],
        USER_ORM_TEST_PARAMS['password'],
        USER_ORM_TEST_PARAMS['salt']
    )

    try:
        with transaction_state_manager:
            transaction_state_manager.card_repos.set_item(card)
            transaction_state_manager.user_repos.set_item(user)

            raise ValueError('Ошибка во время транзакции!')
    except ValueError:
        pass

    db_session.expunge_all()

    user_login = CARD_ORM_TEST_PARAMS['user_login']
    card_id = CARD_ORM_TEST_PARAMS['card_id']

    login = USER_ORM_TEST_PARAMS['login']

    result_card = db_session.get(CardORM, (user_login, card_id))
    result_user = db_session.get(UserORM, login)

    assert result_card is None, \
        "Карточки пользователя не должно быть в хранилище!"
    assert result_user is None, "Пользователя не должно быть в хранилище!"


def test_not_saved_when_commit_is_not_call(db_session: Session):
    transaction_state_manager = TransactionStateManager(
        lambda: db_session  # type: ignore
    )

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

    user = User(
        Settings(
            USER_ORM_TEST_PARAMS['name'],
            Path(USER_ORM_TEST_PARAMS['avatar_path']),
            USER_ORM_TEST_PARAMS['time_block']
        ),
        USER_ORM_TEST_PARAMS['login'],
        USER_ORM_TEST_PARAMS['password'],
        USER_ORM_TEST_PARAMS['salt']
    )

    with transaction_state_manager:
        transaction_state_manager.card_repos.set_item(card)
        transaction_state_manager.user_repos.set_item(user)

    db_session.expunge_all()

    user_login = CARD_ORM_TEST_PARAMS['user_login']
    card_id = CARD_ORM_TEST_PARAMS['card_id']

    login = USER_ORM_TEST_PARAMS['login']

    result_card = db_session.get(CardORM, (user_login, card_id))
    result_user = db_session.get(UserORM, login)

    assert result_card is None, \
        "Карточки пользователя не должно быть в хранилище!"
    assert result_user is None, "Пользователя не должно быть в хранилище!"

# === Негативные тесты ===
def test_commit_raises_session_is_not_initialized():
    transaction_state_manager = TransactionStateManager(
        lambda: None  # type: ignore
    )

    with pytest.raises(SessionIsNotInitializedError):
        with transaction_state_manager:
            transaction_state_manager.commit()


def test_rollback_raises_session_is_not_initialized():
    transaction_state_manager = TransactionStateManager(
        lambda: None  # type: ignore
    )

    with pytest.raises(SessionIsNotInitializedError):
        with transaction_state_manager:
            transaction_state_manager.rollback()

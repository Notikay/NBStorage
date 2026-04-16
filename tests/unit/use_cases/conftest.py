from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from domain.entities import MetaData, Card, Settings, User
from domain.interfaces.units.card import CardUnitOfWorkInterface
from domain.interfaces.units.user import UserUnitOfWorkInterface

if TYPE_CHECKING:
    from pytest import FixtureRequest
    from pytest_mock import MockFixture, MockType

    from tests.unit.use_cases.test_card_use_cases import TestCard
    from tests.unit.use_cases.test_user_use_cases import TestUser


def _get_test_params(
        req_cls,
        addl_params_name: str,
        params_name: str
):
    addl_test_params = getattr(req_cls, addl_params_name, None)
    test_params = getattr(req_cls, params_name, None)
    if (addl_test_params is None) or (test_params is None):
        pytest.fail(
            f"Класс тестов {req_cls.__name__} не имеет атрибута "
            f"{addl_params_name} или {params_name}, с тестовыми "
            "параметрами для карточки пользователя."
        )
    elif not (addl_test_params and test_params):
        pytest.fail(
             f"Класс тестов {req_cls.__name__} имеет атрибуты "
             f"{addl_params_name} и {params_name}, но тестовые параметры "
             "отсутствуют."
        )

    return addl_test_params, test_params

def _create_card(req_cls: TestCard):
    metadata_test_params, card_test_params = _get_test_params(
        req_cls,
        'METADATA_TEST_PARAMS',
        'CARD_TEST_PARAMS'
    )

    card = Card(MetaData(*metadata_test_params), *card_test_params)
    card.encrypt()

    return card

def _create_user(req_cls: TestUser):
    settings_test_params, user_test_params = _get_test_params(
        req_cls,
        'SETTINGS_TEST_PARAMS',
        'USER_TEST_PARAMS'
    )

    user = User(Settings(*settings_test_params), *user_test_params)
    user.hash_password()

    return user

@pytest.fixture
def card(request: FixtureRequest) -> Card:
    return _create_card(request.cls)

@pytest.fixture
def another_card(request: FixtureRequest) -> Card:
    return _create_card(request.cls)

@pytest.fixture
def card_upd(request: FixtureRequest, card: Card) -> Card:
    upd_metadata_test_params, upd_card_test_params = _get_test_params(
        request.cls,
        'UPD_METADATA_TEST_PARAMS',
        'UPD_CARD_TEST_PARAMS'
    )

    upd_card = Card(
        MetaData(
            card.metadata.title,
            card.metadata.icon_path,
            card.metadata.user_login,
            card.metadata.key
        ),
        card.username,
        card.email,
        card.password,
        card.url,
        card.description
    )

    (
        upd_card.metadata.title,
        upd_card.metadata.icon_path
    ) = upd_metadata_test_params
    (
        upd_card.username,
        upd_card.email,
        upd_card.password,
        upd_card.url,
        upd_card.description
    ) = upd_card_test_params


    upd_card.encrypt()

    return upd_card

@pytest.fixture
def mock_card_uow(
        mocker: MockFixture,
        card: Card,
        another_card: Card,
        card_upd: Card
) -> MockType:
    mock = mocker.MagicMock(spec=CardUnitOfWorkInterface)

    mock.__enter__.return_value = mock
    mock.card_repos.get_item.return_value = card
    mock.card_repos.get_all_items.return_value = [card, another_card]
    mock.card_repos.set_item.return_value = card
    mock.card_repos.upd_item.return_value = card_upd

    return mock

@pytest.fixture
def user(request: FixtureRequest) -> User:
    return _create_user(request.cls)

@pytest.fixture
def another_user(request: FixtureRequest) -> User:
    return _create_user(request.cls)

@pytest.fixture
def user_upd(request: FixtureRequest, user: User) -> User:
    upd_settings_test_params, upd_user_test_params = _get_test_params(
        request.cls,
        'UPD_SETTINGS_TEST_PARAMS',
        'UPD_USER_TEST_PARAMS'
    )

    upd_user = User(
        Settings(
            user.settings.name,
            user.settings.avatar_path,
            user.settings.time_block
        ),
        user.login,
        user.password
    )

    (
        upd_user.settings.name,
        upd_user.settings.avatar_path,
        upd_user.settings.time_block
    ) = upd_settings_test_params
    upd_user.password = upd_user_test_params[0]

    upd_user.hash_password()

    return upd_user

@pytest.fixture
def mock_user_uow(
        mocker: MockFixture,
        user: User,
        another_user: User,
        user_upd: User
) -> MockType:
    mock = mocker.MagicMock(spec=UserUnitOfWorkInterface)

    mock.__enter__.return_value = mock
    mock.user_repos.get_item.return_value = user
    mock.user_repos.get_all_items.return_value = [user, another_user]
    mock.user_repos.set_item.return_value = user
    mock.user_repos.upd_item.return_value = user_upd

    return mock

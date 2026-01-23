from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from domain.entities import MetaData

if TYPE_CHECKING:
    from pytest import FixtureRequest


@pytest.fixture
def meta(request: FixtureRequest) -> MetaData:
    test_params = getattr(request.cls, 'METADATA_TEST_PARAMS', None)
    if test_params is None:
        pytest.fail(
            f"Класс тестов {request.cls.__name__} не имеет атрибута "
            "METADATA_TEST_PARAMS, с тестовыми параметрами для метаданных "
            "карточки пользователя."
        )
    return MetaData(*test_params)

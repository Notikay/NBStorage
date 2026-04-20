from __future__ import annotations

from typing import Literal, TYPE_CHECKING

import pytest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.persistence.models.base import Base

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from sqlalchemy.engine import Engine

type DBNameType = Literal['sqlite']


def _get_db_url(name: DBNameType):
    match name:
        case 'sqlite':
            return "sqlite:///:memory:"
        case _:
            pytest.fail(f"Базы данных с именем '{name}' не существует!")

@pytest.fixture(scope='session', params=['sqlite'])
def engine(request: FixtureRequest) -> Engine:
    name = request.param
    db_url = _get_db_url(name)

    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    return engine

@pytest.fixture()
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from duno_fast_zero.app import app
from duno_fast_zero.models import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    # Cria um banco de dados em memória
    engine = create_engine('sqlite:///:memory:')

    # Cria toda a estrutura do banco
    # a partir desses metadados usando a engine, plz
    # Singleton -> cria todas as tabelas com apenas uma chamada

    # Setup
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Tear down
    table_registry.metadata.drop_all(engine)

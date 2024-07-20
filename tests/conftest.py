import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from duno_fast_zero.app import app
from duno_fast_zero.database import get_session
from duno_fast_zero.models import User, table_registry
from duno_fast_zero.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}+senha')


@pytest.fixture()
def client(session):
    def get_sesion_override():
        return session

    with TestClient(app) as client:
        # Troca a dependência get_session por get_sesion_override
        app.dependency_overrides[get_session] = get_sesion_override
        yield client

    # Depois que o teste terminar, limpa as dependências
    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    # Cria um banco de dados em memória
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # Cria toda a estrutura do banco
    # a partir desses metadados usando a engine, plz
    # Singleton -> cria todas as tabelas com apenas uma chamada

    # Setup
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Tear down
    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = 'testtest'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    # Monkey patch: alterando atributo em tempo de execução
    user.clean_password = pwd

    return user


@pytest.fixture()
def other_user(session):
    pwd = 'testtest'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    # Monkey patch: alterando atributo em tempo de execução
    user.clean_password = pwd

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )
    return response.json()['access_token']

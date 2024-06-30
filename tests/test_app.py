from http import HTTPStatus

from fastapi.testclient import TestClient

from duno_fast_zero.app import app


def test_read_root_must_return_ok_and_hello_world():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, galera!'}


def test_read_root_must_return_ok_and_ola_mundo_html():
    client = TestClient(app)
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert '<html>' in response.text
    assert 'olá mundo' in response.text

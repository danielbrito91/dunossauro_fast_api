from http import HTTPStatus

import pytest


def test_read_root_must_return_ok_and_hello_world(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, galera!'}


@pytest.mark.skip(reason='Aula 02 - exercício')
def test_read_root_must_return_ok_and_ola_mundo_html(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert '<html>' in response.text
    assert 'olá mundo' in response.text


def test_create_user_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'new_user_name',
            'password': 'password',
            'email': user.email,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_ex_01_must_return_ok_and_ola_mundo_html(client):
    response = client.get('/ex01')

    assert response.status_code == HTTPStatus.OK
    assert '<html>' in response.text
    assert 'olá mundo' in response.text

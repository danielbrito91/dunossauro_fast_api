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


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'johndoe',
            'password': 'password',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'johndoe',
        'email': 'test@test.com',
    }


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'johndoe', 'email': 'test@test.com'}]
    }


def test_read_single_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'johndoe',
        'email': 'test@test.com',
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'password': 'password',
            'username': 'fulano de tal',
            'email': 'test@test.com',
            'id': 1,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'fulano de tal',
        'email': 'test@test.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/999',
        json={
            'password': 'password',
            'username': 'fulano de tal',
            'email': 'email@email.com',
            'id': 999,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete(
        '/users/1',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete(
        '/users/999',
    )
    assert response.status_code == HTTPStatus.NOT_FOUND

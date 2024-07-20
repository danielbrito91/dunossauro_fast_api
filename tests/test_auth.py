from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_token_expire_after_time(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        # Gerar o token
        response = client.post(
            '/auth/token',
            data={
                'username': user.username,
                'password': user.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        # Usa  o token
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'password': 'password',
                'username': 'fulano de tal',
                'email': 'wrong',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.username,
            'password': 'wrong',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_email_password(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': 'blah',
            'password': user.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_inexistent_user(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': 'blah',
            'password': 'wrong',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        # Gerar o token
        response = client.post(
            '/auth/token',
            data={
                'username': user.username,
                'password': user.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        # Usa  o token
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}

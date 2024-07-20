from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from duno_fast_zero.security import (
    create_access_token,
    get_current_user,
    settings,
)


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        'users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_suser_must_return_exception():
    with pytest.raises(HTTPException):
        get_current_user({})


def test_get_current_user_without_sub_must_return_exception(session):
    data = {'bub': 'test@test.com'}
    token = create_access_token(data)

    with pytest.raises(HTTPException):
        get_current_user(session=session, token=token)


def test_get_current_user_with_invalid_email_must_return_exception(session):
    data = {'sub': 'thisemaildoestnotexist@test.com'}
    token = create_access_token(data)

    with pytest.raises(HTTPException):
        get_current_user(session=session, token=token)

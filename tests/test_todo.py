import time
from http import HTTPStatus

import pytest

from duno_fast_zero.models import TodoState
from tests.conftest import TodoFactory


def test_create_todo(client, token, user):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test description',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data['id'] == 1
    assert response_data['title'] == 'Test todo'
    assert response_data['description'] == 'Test description'
    assert response_data['state'] == 'draft'
    assert 'created_at' in response_data
    assert 'updated_at' in response_data
    assert response_data['created_at'] == response_data['updated_at']


def test_list_todo_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    # Bulk save -> coloca uma lista de objetos na Session de uma vez
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.parametrize(
    ('todo_params', 'url', 'expected_todos'),
    [
        (
            {'size': 5},
            '/todos/?offset=1&limit=2',
            2,
        ),
        (
            {'size': 5, 'title': 'Test todo 1'},
            '/todos/?title=Test todo 1',
            5,
        ),
        (
            {'size': 5, 'description': 'description'},
            '/todos/?description=desc',
            5,
        ),
        (
            {'size': 5, 'state': TodoState.draft},
            '/todos/?state=draft',
            5,
        ),
    ],
)
def test_list_todo_filter(  # noqa
    session,
    client,
    token,
    user,
    todo_params,
    url,
    expected_todos,
):
    session.bulk_save_objects(
        TodoFactory.create_batch(user_id=user.id, **todo_params)
    )
    session.commit()

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has ben deleted successfully'}


def test_delete_todo_error(client, token):
    response = client.delete(
        '/todos/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    time.sleep(1)

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'New title',
            'description': 'New description',
            'state': 'done',
        },
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data['id'] == todo.id
    assert response_data['title'] == 'New title'
    assert response_data['description'] == 'New description'
    assert response_data['state'] == 'done'
    assert response_data['created_at'] != response_data['updated_at']


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/999',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}

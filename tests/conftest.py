import pytest
from fastapi.testclient import TestClient

from duno_fast_zero.app import app


@pytest.fixture()
def client():
    return TestClient(app)

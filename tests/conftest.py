import pytest

from main import app


@pytest.fixture
def client():
    yield app.test_client()


from unittest.mock import Mock
import pytest
from src.repositories.status import StatusRepository
from src import settings


@pytest.fixture
def database_connection(monkeypatch):
    monkeypatch.setattr("psycopg2.connect", mock := Mock())
    return mock


@pytest.fixture
def database_setup(monkeypatch):
    monkeypatch.setattr(
        "src.repositories.status.StatusRepository.set_up", mock := Mock()
    )
    return mock


def test_status_repository_connection(database_connection, database_setup):
    StatusRepository()
    database_connection.assert_called_with(settings.DB_URI)
    database_setup.assert_called_with()

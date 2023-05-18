from unittest.mock import Mock

import pytest
from src.consumers.consumer import get_consumer_client
from tenacity import stop_after_attempt


@pytest.fixture
def get_consumer(monkeypatch):
    monkeypatch.setattr(
        "src.services.kafka.KafkaFactory.get_client", mock := Mock()
    )
    return mock


@pytest.fixture
def get_consumer_with_exception(monkeypatch):
    monkeypatch.setattr(
        "src.services.kafka.KafkaFactory.get_client", mock := Mock()
    )
    mock.side_effect = Exception
    return mock


@pytest.fixture
def mock_process_message(monkeypatch):
    monkeypatch.setattr(
        "src.consumers.consumer.StatusProcessor.process_message",
        mock := Mock(),
    )
    return mock


@pytest.fixture
def mock_status_repository(monkeypatch):
    monkeypatch.setattr(
        "src.consumers.consumer.StatusRepository", mock := Mock()
    )
    return mock


def test_get_consumer_client(get_consumer):
    get_consumer_client()
    get_consumer.assert_called_with(producer=False)


def test_get_consumer_client_returns_exception(
    get_consumer_with_exception, caplog
):
    get_consumer_client.retry.stop = stop_after_attempt(1)
    with pytest.raises(Exception):
        get_consumer_client()
    assert "Exception while getting client " in caplog.messages
    get_consumer_with_exception.assert_called_with(producer=False)

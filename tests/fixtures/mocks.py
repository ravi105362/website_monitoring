import pytest
from unittest.mock import Mock


@pytest.fixture
def get_producer(monkeypatch):
    monkeypatch.setattr(
        "src.services.kafka.KafkaFactory.get_client", mock := Mock()
    )
    return mock


@pytest.fixture
def mock_get_producer_client(monkeypatch):
    monkeypatch.setattr("src.services.kafka.KafkaProducer", mock := Mock())
    return mock


@pytest.fixture
def mock_get_consumer_client(monkeypatch):
    monkeypatch.setattr("src.services.kafka.KafkaConsumer", mock := Mock())
    return mock

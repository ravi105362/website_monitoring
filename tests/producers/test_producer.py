from unittest.mock import Mock
import pytest
from src.producers.producer import get_producer_client, publish_website_status


@pytest.fixture
def mock_producer_send(monkeypatch, get_producer):
    monkeypatch.setattr(
        "src.producers.producer.KafkaFactory.get_client", mock := Mock()
    )
    return mock


@pytest.fixture
def mock_get_list_of_websites(monkeypatch):
    monkeypatch.setattr(
        "src.producers.producer.get_list_of_websites", mock := Mock()
    )
    mock.return_value = ["www.abc.com", "www.def.com"]
    return mock


def test_get_producer_client(get_producer):
    get_producer_client()
    get_producer.assert_called_with(producer=True)


def test_publish_website_status(get_producer, mock_get_list_of_websites):
    publish_website_status()
    get_producer.assert_called_with(producer=True)
    mock_get_list_of_websites.assert_called_with()

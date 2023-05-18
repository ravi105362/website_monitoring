import json
from unittest.mock import Mock
import pytest
from src.processor.processor import StatusProcessor
from src import settings
from kafka.consumer.fetcher import ConsumerRecord


@pytest.fixture
def mock_check_status_exists(monkeypatch):
    monkeypatch.setattr(
        "src.processor.processor.check_status_exists", mock := Mock()
    )
    return mock


@pytest.fixture
def mock_check_website_exists(monkeypatch):
    monkeypatch.setattr(
        "src.processor.processor.check_website_exists", mock := Mock()
    )
    return mock


@pytest.fixture
def mock_insert_status(monkeypatch):
    monkeypatch.setattr(
        "src.processor.processor.insert_status", mock := Mock()
    )
    return mock


@pytest.fixture
def mock_update_timestamp(monkeypatch):
    monkeypatch.setattr(
        "src.processor.processor.update_timestamp", mock := Mock()
    )
    return mock


@pytest.fixture
def mock_insert_websites(monkeypatch):
    monkeypatch.setattr(
        "src.processor.processor.insert_websites", mock := Mock()
    )
    return mock


@pytest.fixture
def mock_cursor(monkeypatch):
    monkeypatch.setattr(
        "src.processor.processor.StatusProcessor", "cur", mock := Mock()
    )
    return mock


def test_process_message(
    mock_check_status_exists,
    mock_check_website_exists,
    mock_insert_status,
    mock_update_timestamp,
    mock_insert_websites,
):
    mock = Mock()
    mock.fetchone.return_value = [1, 2, 3]
    processor = StatusProcessor(cur=mock)
    message = ConsumerRecord(
        topic=settings.AIVEN_KAFKA_WEBSITE_TOPIC,
        partition=0,
        offset=1,
        timestamp=1683453430,
        timestamp_type="",
        headers={},
        checksum="",
        serialized_header_size=0,
        serialized_key_size=0,
        serialized_value_size=0,
        key=json.dumps("https://test.com").encode("utf-8"),
        value={
            "response_code": 200,
            "response_time": 10,
        },
    )
    processor.process_message(message=message)

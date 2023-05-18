from unittest.mock import ANY
from src.services.kafka import ClientConfig, KafkaFactory
from src import settings


def test_client_config():
    config = ClientConfig("https://abc.com", "ca.pem", "cert.pem", "key.pem")

    assert config.bootstrap_servers == "https://abc.com"
    assert config.security_protocol == "SSL"
    assert config.ssl_cafile == "ca.pem"
    assert config.ssl_certfile == "cert.pem"
    assert config.ssl_keyfile == "key.pem"


def test_kafka_factory_producer(mock_get_producer_client):
    client = KafkaFactory()
    client.get_client(producer=True)
    mock_get_producer_client.assert_called_with(
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        security_protocol="SSL",
        ssl_cafile=ANY,
        ssl_certfile=ANY,
        ssl_keyfile=ANY,
        value_serializer=ANY,
        key_serializer=ANY,
    )


def test_kafka_factory_consumer(mock_get_consumer_client):
    client = KafkaFactory()
    client.get_client()
    mock_get_consumer_client.assert_called_with(
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        security_protocol="SSL",
        ssl_cafile=ANY,
        ssl_certfile=ANY,
        ssl_keyfile=ANY,
        value_deserializer=ANY,
        auto_offset_reset="earliest",
    )

import json
from src import settings
from kafka import KafkaProducer, KafkaConsumer
from dataclasses import dataclass


@dataclass
class ClientConfig:
    """
    Class stores all the configs. for producer and consumer
    """

    bootstrap_servers: str
    security_protocol = "SSL"
    ssl_cafile: str
    ssl_certfile: str
    ssl_keyfile: str


class KafkaFactory:
    """
    Kafka Factory which returns objects based on requirement
    """

    @staticmethod
    def get_client(producer: bool = False):
        config = ClientConfig(
            bootstrap_servers=settings.BOOTSTRAP_SERVER,
            ssl_cafile=settings.SSL_CAFILE,
            ssl_certfile=settings.SSL_CERTFILE,
            ssl_keyfile=settings.SSL_KEYFILE,
        )

        if producer is True:
            return KafkaProducer(
                bootstrap_servers=config.bootstrap_servers,
                security_protocol=config.security_protocol,
                ssl_cafile=config.ssl_cafile,
                ssl_certfile=config.ssl_certfile,
                ssl_keyfile=config.ssl_keyfile,
                value_serializer=lambda v: json.dumps(v).encode("ascii"),
                key_serializer=lambda v: json.dumps(v).encode("ascii"),
            )
        else:
            return KafkaConsumer(
                bootstrap_servers=config.bootstrap_servers,
                security_protocol=config.security_protocol,
                ssl_cafile=config.ssl_cafile,
                ssl_certfile=config.ssl_certfile,
                ssl_keyfile=config.ssl_keyfile,
                value_deserializer=lambda v: json.loads(v.decode("ascii")),
                auto_offset_reset="earliest",
            )

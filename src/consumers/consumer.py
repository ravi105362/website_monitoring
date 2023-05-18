import os
from tenacity import retry, wait_exponential, retry_if_result

from src import settings
from src.services.kafka import KafkaFactory
from src.repositories.status import StatusRepository
from src.processor.processor import StatusProcessor
from src.utils.util import is_none_p, get_logger

logging = get_logger()


@retry(
    wait=wait_exponential(multiplier=1, max=10),
    retry=(retry_if_result(is_none_p)),
)
def get_consumer_client():
    try:
        consumer = KafkaFactory.get_client(producer=False)
        consumer.subscribe(topics=settings.AIVEN_KAFKA_WEBSITE_TOPIC)
        return consumer
    except Exception as exc:
        logging.error(f"Exception while getting client {exc}")
        return None


def get_website_status():
    """
    Consumer reads data from the broker and process it
    """

    consumer = get_consumer_client()
    repo = StatusRepository()
    processor = StatusProcessor(cur=repo.cur)

    for message in consumer:
        try:
            processor.process_message(message)
        except Exception as exc:
            logging.error(
                f"Error during processing {message} with Exception\
                 {exc}"
            )

        repo.do_commit()


if __name__ == "__main__":
    get_website_status()

import os
from tenacity import retry, wait_exponential, retry_if_result

from src.services.kafka import KafkaFactory
from src import settings
from src.utils.util import get_logger
from src.utils.util import get_list_of_websites, get_website_status, is_none_p

logging = get_logger()


@retry(
    wait=wait_exponential(multiplier=1, max=10),
    retry=(retry_if_result(is_none_p)),
)
def get_producer_client():
    try:
        producer = KafkaFactory.get_client(producer=True)
        return producer
    except Exception as exc:
        logging.error(f"Exception while getting client {exc}")
        return None


def publish_website_status():
    """
    Checks the status of URL and pushes the data to broker
    """

    websites = get_list_of_websites()
    producer = get_producer_client()

    for website in websites:
        resp = get_website_status(website)
        if resp is None:
            continue

        try:
            producer.send(
                topic=settings.AIVEN_KAFKA_WEBSITE_TOPIC,
                key={"key": website},
                value={
                    "response_code": resp.status_code,
                    "response_time": resp.elapsed.total_seconds(),
                },
            )
            logging.info(f"Message sent for {website}")
        except Exception as exc:
            logging.error(f"For {website} Exception found {exc}")

        producer.flush()


if __name__ == "__main__":
    publish_website_status()

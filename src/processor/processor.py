import json
from dataclasses import dataclass
import os

from src.utils.queries import (
    check_status_exists,
    check_website_exists,
    insert_status,
    update_timestamp,
    insert_websites,
)
from src import settings
from src.utils.util import get_logger

logging = get_logger()


@dataclass
class StatusProcessor:
    """
    Processes the messages recieved by the consumer
    """

    cur: any

    def process_message(self, message):
        key: dict = json.loads(message.key.decode("ascii"))

        if check_website_exists(self.cur, key) == 0:
            insert_websites(self.cur, key)
            check_website_exists(self.cur, key)

        element_id = self.cur.fetchone()[0]

        if check_status_exists(self.cur, element_id, message) == 0:
            insert_status(self.cur, element_id, message)
        else:
            update_timestamp(self.cur, element_id, message)

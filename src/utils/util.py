import json
from pathlib import Path
import requests
import logging
import os
import re
from src import settings

p = Path(__file__).with_name("website_data.json")


def get_website_status(website):
    try:
        resp = requests.get(website, timeout=settings.TIMEOUT)
    except Exception as exc:
        logging.error(f"Could not process website due to {exc}")
        return None

    title = re.search(r"<\W*title\W*(.*)</title", resp.text, re.IGNORECASE)

    if title is not None and get_title(website) != title.group(1):
        resp.status_code = 422
        logging.error(f"Title does not match expected for {website}")

    return resp


def get_list_of_websites():
    websites = []

    with p.open("r") as f:
        data = json.load(f)
        for website in data["websites"]:
            websites.append(website["url"])

    return websites


def get_title(url):
    title = ""
    with p.open("r") as f:
        data = json.load(f)
        for website in data["websites"]:
            if website["url"] == url:
                title = website["title"]
    return title


def is_none_p(value):
    """Return True if value is None"""
    return value is None


def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        filename=os.path.join(settings.LOGGER_FOLDER),
        format="%(asctime)s :: %(levelname)s :: %(message)s",
    )
    return logging


logging = get_logger()

from datetime import datetime as dt


def check_website_exists(cur, key):
    """
    Checks if the same URL already exists in the websites table
    """
    cur.execute("SELECT id FROM websites WHERE url =%s;", (key["key"],))
    return cur.rowcount


def check_status_exists(cur, element_id, message):
    """
    Checks if the same status for same website already exists
    """
    cur.execute(
        "SELECT website_id FROM status WHERE website_id =%s and\
             status=%s;",
        (element_id, message.value["response_code"]),
    )
    return cur.rowcount


def insert_websites(cur, key):
    """
    Inserts a newly found URL in the websites table
    """
    cur.execute("INSERT INTO websites (url) VALUES (%s);", (key["key"],))


def insert_status(cur, element_id, message):
    """
    Inserts status for the URLs
    """
    cur.execute(
        "INSERT INTO status (website_id,status,ts) VALUES (%s,%s, %s);",
        (
            element_id,
            message.value["response_code"],
            dt.fromtimestamp(message.timestamp / 1000),
        ),
    )


def update_timestamp(cur, element_id, message):
    """
    Updates the timestamp of the URLs in the status table
    """
    cur.execute(
        "UPDATE status SET ts = %s WHERE website_id = %s and status = %s",
        (
            dt.fromtimestamp(message.timestamp / 1000),
            element_id,
            message.value["response_code"],
        ),
    )

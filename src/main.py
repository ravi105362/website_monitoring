from fastapi import BackgroundTasks, FastAPI
import uvicorn
import os
import time
import threading
from src.producers import producer
from src.consumers import consumer
from src.utils.util import get_logger
import settings

app = FastAPI()

logging = get_logger()


class BackgroundTasksProducer(threading.Thread):
    """
    For running the producer
    """

    def run(self, *args, **kwargs):
        while True:
            try:
                producer.publish_website_status()
            except Exception as exc:
                logging.error(f"Could not send message to broker {exc}")
            time.sleep(100)


class BackgroundTasksConsumer(threading.Thread):
    """
    For running the consumer
    """

    def run(self, *args, **kwargs):
        while True:
            try:
                consumer.get_website_status()
            except Exception as exc:
                logging.error(f"Could not process message from broker {exc}")


@app.on_event("startup")
async def startup_event():
    s = BackgroundTasksConsumer()
    t = BackgroundTasksProducer()
    s.start()
    t.start()


@app.get("/")
async def root(background_tasks: BackgroundTasks):
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)

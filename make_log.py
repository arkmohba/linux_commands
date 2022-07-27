import json
from logging import getLogger, config
import random
import threading
import time

with open('log_config.json', 'r') as f:
    log_conf = json.load(f)

config.dictConfig(log_conf)

# ここからはいつもどおり
logger = getLogger(__name__)


def work():
    for _ in range(3):
        logger.info("Received")
        time.sleep(random.random())
        logger.info("Calculate START")
        time.sleep(5*random.random())
        logger.info("Calculate END")
        time.sleep(random.random())
        logger.info("Replied")


def main():
    logger.info("START")
    threads = []
    for _ in range(3):
        thread = threading.Thread(target=work)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    logger.info("END")


if __name__ == "__main__":
    main()

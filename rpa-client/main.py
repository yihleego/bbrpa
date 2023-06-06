import logging
import os
import signal
import sys
import time

import config
from scheduler import Scheduler


def init():
    formatter = logging.Formatter(config.logging.format)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(config.logging.level)
    logger.addHandler(stream_handler)
    if config.logging.filename:
        os.makedirs(os.path.dirname(config.logging.filename), exist_ok=True)
        file_handler = logging.FileHandler(config.logging.filename, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    signal.signal(signal.SIGINT, lambda *args: sys.exit())
    signal.signal(signal.SIGTERM, lambda *args: sys.exit())


def run():
    while True:
        scheduler = Scheduler(
            host=config.server.host,
            port=config.server.port,
            path=config.server.path,
            ssl=config.server.ssl,
            app_size=config.app.size)
        scheduler.startup()
        logging.error(
            'Unable to connect to the server host: %s, port: %d, path: %s, ssl: %s',
            config.server.host, config.server.port, config.server.path, config.server.ssl)
        scheduler.shutdown()
        time.sleep(5)


if __name__ == '__main__':
    init()
    run()

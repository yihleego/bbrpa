# -*- coding=utf-8
import logging
import os
import signal
import sys
import threading

import config
from rpa import RPA


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


def run():
    def startup():
        logging.info("Starting")
        event.clear()
        rpa.startup()
        while not event.isSet():
            rpa.handle()

    def shutdown(signum, frame):
        logging.info("Stopping %d %s", signum, str(frame))
        event.set()
        rpa.shutdown()

    event = threading.Event()
    rpa = RPA(event)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    startup()


if __name__ == '__main__':
    init()
    run()

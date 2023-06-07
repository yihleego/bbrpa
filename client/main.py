import logging
import os
import signal
import sys
import threading

from rpa import RPA


def init():
    formatter = logging.Formatter('%(asctime)s %(levelname)-5s [%(process)d-%(thread)d-%(threadName)s] %(module)s#%(funcName)s : %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    os.makedirs(os.path.dirname('./logs/rpa-client.log'), exist_ok=True)
    file_handler = logging.FileHandler('./logs/rpa-client.log', encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    signal.signal(signal.SIGINT, lambda *args: sys.exit())
    signal.signal(signal.SIGTERM, lambda *args: sys.exit())


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

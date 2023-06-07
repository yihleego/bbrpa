import logging
import os
import signal
import sys
import threading
from abc import ABC
from queue import PriorityQueue

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class App:
    def __init__(self, driver):
        self.driver = driver
        self.status = 0
        self.event = threading.Event()
        self.delay = 0

    def stop(self):
        self.event.set()

    def run(self):
        while not self.event.isSet():
            self.loop()
            if self.delay > 0:
                self.event.wait(self.delay)

    def loop(self):
        logging.info('app run')
        self.delay = 5


class Handler(ABC):
    def start(self):
        pass

    def stop(self):
        pass

    def handle(self):
        pass


class MainHandler(Handler):
    def __init__(self):
        self.app_handler = AppHandler()
        self.health_handler = HealthHandler()

    def start(self):
        self.app_handler.start()
        self.health_handler.start()

    def stop(self):
        self.app_handler.stop()
        self.health_handler.stop()

    def run(self):
        self.app_handler.handle()
        self.health_handler.handle()


class AppHandler(Handler):
    def __init__(self, max_apps=2):
        self.max_apps: int = max_apps
        self.apps: [App] = []

    def stop(self):
        for app in self.apps:
            app.stop()

    def handle(self):
        if len(self.apps) < self.max_apps:
            for i in range(self.max_apps - len(self.apps)):
                app = App(self.new_driver())
                self.apps.append(app)
                thread = threading.Thread(target=app.run, daemon=True)
                thread.start()

    def new_driver(self) -> WebDriver:
        # prefs = {"profile.default_content_settings": {"images": 2}}

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.experimental_options["prefs"] = prefs

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

        return Chrome(options=options, desired_capabilities=capabilities)


class HealthHandler(Handler):
    def __init__(self):
        pass


class TaskHandler(Handler):
    def __init__(self):
        self.tasks = PriorityQueue()


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
    def start():
        logging.info("Starting")
        event.clear()
        main.start()
        while not event.isSet():
            main.run()
            event.wait(1)

    def stop(signum, frame):
        logging.info("Stopping %d %s", signum, str(frame))
        event.set()
        main.stop()

    event = threading.Event()
    main = MainHandler()
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    start()


if __name__ == '__main__':
    init()
    run()

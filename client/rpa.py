import threading
from abc import ABC

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from app import App


class Service(ABC):
    def startup(self):
        pass

    def shutdown(self):
        pass

    def handle(self):
        pass


class RPA(Service):
    def __init__(self, event: threading.Event):
        self.event: threading.Event = event
        self.app_manager = AppManager()
        self.health_manager = HealthManager()

    def startup(self):
        self.app_manager.startup()
        self.health_manager.startup()

    def shutdown(self):
        self.app_manager.shutdown()
        self.health_manager.shutdown()

    def handle(self):
        self.app_manager.handle()
        self.health_manager.handle()
        self.wait()

    def wait(self):
        self.event.wait(10)


class AppManager(Service):
    def __init__(self, max_apps=1):
        self.max_apps: int = max_apps
        self.apps: [App] = []

    def shutdown(self):
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
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        return Chrome(options=options, desired_capabilities=capabilities)


class HealthManager(Service):
    def __init__(self):
        pass

    def handle(self):
        pass
        # body = {}
        # with requests.post("http://localhost:11111/health", json=body, verify=False, timeout=10) as resp:
        #     if resp.status_code < 300:
        #         return True, None
        #     else:
        #         return False, str(resp)

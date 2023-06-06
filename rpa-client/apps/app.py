import json
import time

from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class ClientStatus:
    OFFLINE = 0
    ONLINE = 1
    WAITING = 2
    ERROR = 3
    SUSPENDED = 4


class TaskStatus:
    CREATED = 0
    RUNNING = 1
    DELETED = 2
    CANCELLED = 3
    FINISHED = 10
    FAILED = 11
    TIMEOUT = 12
    OFFLINE = 13
    TERMINATED = 14
    UNSUPPORTED = 15


class User:
    def __init__(self, id, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password


class App:
    def __init__(self, driver: WebDriver, status: int = None, user=None):
        self.driver = driver
        self.status = status
        self.user = user

    @classmethod
    def launch(cls, number: int = 1):
        clients = []
        for i in range(number):
            options = Options()
            options.add_argument('--headless')
            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
            driver = WebDriver(options=options, desired_capabilities=capabilities)
            clients.append(driver)

    def execute(self, task_type, task_data=None):
        func = getattr(self, task_type)
        if not func:
            raise NotImplementedError
        return func(task_data)

    def translate(self, data):
        # TODO 测试
        driver: WebDriver = self.driver
        driver.get('https://fanyi.baidu.com/#en/zh/')
        driver.find_element(by=By.CSS_SELECTOR, value='#baidu_translate_input').send_keys(data["text"])
        driver.find_element(by=By.CSS_SELECTOR, value='#baidu_translate_input').send_keys(Keys.ENTER)

        time.sleep(1)
        logs = driver.get_log('performance')
        for log in logs:
            data = json.loads(log["message"])
            type = get_value(data, ["message", "method"])
            url = get_value(data, ["message", "params", "response", "url"])
            if type is not None \
                    and url is not None \
                    and type.find("Network.response") >= 0 \
                    and url.find("https://fanyi.baidu.com/v2transapi?from=en&to=zh") >= 0:
                try:
                    request_id = get_value(data, ["message", "params", "requestId"])
                    mime_type = get_value(data, ["message", "params", "response", "mimeType"])
                    if mime_type == "application/json":
                        res = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                        body = json.loads(res["body"])
                        trans = body["trans_result"]["data"]
                        return trans[0]["dst"] if len(trans) > 0 else None
                except Exception as e:
                    print(e)


def get_value(data, keys):
    for k in keys:
        if k in data:
            data = data[k]
        else:
            return None
    return data

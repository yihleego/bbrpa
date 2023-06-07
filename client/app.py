import json
import logging
import threading
import time
from queue import Queue

import requests
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class App:
    def __init__(self, driver: WebDriver):
        self.event = threading.Event()
        self.driver: WebDriver = driver
        self.status: int = 0
        self.delay: int = 0
        self.tasks: Queue = Queue()

    def stop(self):
        self.event.set()
        self.driver.quit()

    def run(self):
        while not self.event.isSet():
            self.loop()
            if self.delay > 0:
                self.event.wait(self.delay)

    def loop(self):
        logging.info('app run')
        if self.tasks.qsize() > 0:
            res = self.exec_task(self.tasks.get_nowait())
            self.update_task(res)
            self.delay = 0  # execute next task without delay
        elif self.fetch_tasks():
            self.delay = 0  # execute the fetched task immediately
        else:
            self.delay = 10  # wait if no new tasks

    def exec_task(self, task):
        """
        Execute a task
        """
        try:
            func = getattr(self, task["task_name"])
            if not func:
                raise NotImplementedError
            result = func(task["data"])
            return {
                "id": task["id"],
                "result": result,
                "success": True,
                "message": None,
            }
        except Exception as e:
            logging.exception("Failed to execute task: %s", str(task))
            return {
                "id": task["id"],
                "result": None,
                "success": False,
                "message": str(e)
            }

    def update_task(self, res):
        try:
            with requests.patch("http://localhost:11111/tasks/records", json=res, verify=False, timeout=10) as resp:
                if resp.status_code < 300:
                    return True
                else:
                    logging.error("Failed to update tasks: %s", str(resp))
                    return False
        except:
            logging.exception("Failed to update task: %s", str(res))

    def fetch_tasks(self):
        try:
            with requests.get("http://localhost:11111/tasks/records", verify=False, timeout=310) as resp:
                if resp.status_code < 300:
                    tasks = resp.json()
                    if len(tasks) == 0:
                        return False  # no tasks
                    for t in tasks:
                        self.tasks.put_nowait(t)
                    return True
                else:
                    logging.error("Failed to fetch tasks: %s", str(resp))
                    return False
        except:
            logging.exception("Failed to fetch tasks")

    def get_icons(self, data):
        """
        For testing
        """
        params = json.loads(data)
        driver = self.driver
        keyword = params["keyword"]

        # open url
        driver.get('https://www.iconfont.cn/')
        time.sleep(0.5)

        # toggle the button
        driver.find_element(by=By.CSS_SELECTOR, value='#J_search-box > div:nth-child(1)').click()
        # choose the illustration
        driver.find_element(by=By.CSS_SELECTOR, value='div[data-type=illustration]').click()
        # input the keyword
        driver.find_element(by=By.CSS_SELECTOR, value='input#J_search_input_index').send_keys(keyword + Keys.ENTER)
        time.sleep(0.5)

        # find all images and names
        names = driver.find_elements(by=By.CSS_SELECTOR, value='.block-icon-list>li>.icon-name')
        images = driver.find_elements(by=By.CSS_SELECTOR, value='.block-icon-list>li>.icon-twrap>img')

        result = [{
            "name": names[i].get_property("title"),
            "image": images[i].get_property("src"),
        } for i in range(len(images))]

        return json.dumps(result, ensure_ascii=False)

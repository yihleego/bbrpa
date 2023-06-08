# -*- coding=utf-8
import logging
import threading
from functools import lru_cache
from queue import Queue
from typing import Union

import requests
from selenium.webdriver.chrome.webdriver import WebDriver


class Script:
    id: int
    version: int
    script: str
    params: dict
    func: str

    def init(self):
        lines = self.script.split('\n')
        formatted = '\n\t'.join(lines)
        self.func = f"def task_{self.id}_{self.version}(driver, params):\n\t{formatted}"

    def exec(self, driver, params):
        loc = {"driver": driver, "params": params, "result": None, "success": True}
        exec(self.script, globals(), loc)
        return loc["result"], loc["success"]


class ScriptManager:
    @lru_cache(maxsize=1024)
    def get_script(self, id, version):
        """
        Get script from cache or remote, thread safe.
        """
        res = self.fetch_script(id, version)
        if res is None:
            raise NotImplementedError
        script = Script()
        script.id = res["id"]
        script.version = res["version"]
        script.script = res["script"]
        script.params = res["params"]
        script.init()
        return script

    def fetch_script(self, id, version) -> Union[dict, None]:
        try:
            with requests.get(f"http://localhost:11111/tasks/scripts?id={id}&version={version}", verify=False, timeout=10) as resp:
                if resp.status_code == 200:
                    return resp.json()
                else:
                    logging.error("Failed to get script: %s", str(resp))
                    return None
        except:
            logging.exception("Failed to get script: id=%d version=%d", id, version)
        return None


script_manager = ScriptManager()


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
        record_id = task["id"]
        try:
            script = script_manager.get_script(task["task_id"], task["task_version"])
            if script is None:
                raise NotImplementedError
            result, success = script.exec(self.driver, task["params"])
            return {
                "id": record_id,
                "result": result,
                "success": success,
                "message": None,
            }
        except Exception as e:
            logging.exception("Failed to execute task: %s", str(task))
            return {
                "id": record_id,
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

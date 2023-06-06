import json
import time
from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

executor = ThreadPoolExecutor(max_workers=40, thread_name_prefix="huadong")
pool = []


def exec(data):
    idx: int = data["id"]
    driver: WebDriver = data["driver"]

    # 打开链接
    driver.get('http://baidu.com')
    # 新增 Cookie
    driver.add_cookie({'name': 'test_idx', 'value': str(idx)})
    # 输入关键字
    driver.find_element(by=By.ID, value='kw').send_keys('RPA' + str(idx))
    # 点击搜索
    driver.find_element(by=By.ID, value='su').click()

    time.sleep(2)

    performance_log = driver.get_log('performance')
    print(str(performance_log).strip('[]'))

    for entry in performance_log:
        print(entry)

    test = driver.get_cookie('test_idx')
    print('cookie', str(idx) == test.get("value"), idx, test)

    driver.save_screenshot(f'./temp/{idx}_ch_cookie_{test["value"]}.png')
    driver.quit()


def exec2(data):
    driver: WebDriver = data["driver"]
    driver.get('https://fanyi.baidu.com/#en/zh/')
    driver.find_element(by=By.CSS_SELECTOR, value='#baidu_translate_input').send_keys('Golden')
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
                    print(res["body"], trans)
                    # [{'dst': '金的', 'src': 'Golden'}]
            except Exception as e:
                print(e)

    driver.quit()


def get_value(data, keys):
    for k in keys:
        if k in data:
            data = data[k]
        else:
            return None
    return data


def launch(num: int):
    for i in range(num):
        options = Options()
        options.add_argument('--headless')
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        driver = WebDriver(options=options, desired_capabilities=capabilities)
        pool.append({"id": i, "driver": driver})


def run():
    for data in pool:
        executor.submit(exec2, data=data)


if __name__ == "__main__":
    launch(1)
    run()

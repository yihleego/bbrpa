import json
import time

import waitress
from flask import Flask
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

app = Flask(__name__)


@app.get("/<kw>")
def index(kw):
    driver = new_driver()
    res = exec(driver, kw)
    return res, 200


def new_driver():
    prefs = {
        "profile.default_content_settings": {"images": 2}
    }

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.experimental_options["prefs"] = prefs

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)
    return driver


def exec(driver, kw):
    res = None

    driver.get('https://fanyi.baidu.com/#en/zh/')
    driver.find_element(by=By.CSS_SELECTOR, value='#baidu_translate_input').send_keys(kw)
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
                    res = trans
                    # [{'dst': '金的', 'src': 'Golden'}]
            except Exception as e:
                print(e)

    driver.close()
    return res


def get_value(data, keys):
    for k in keys:
        if k in data:
            data = data[k]
        else:
            return None
    return data


if __name__ == "__main__":
    waitress.serve(app, host="0.0.0.0", port=18000)

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def run_one(url, js, br=None, sleep_second=0, start_sleep=1):
    if br is None:
        browser = get_browser()
    else:
        browser = br
    browser.get(url)
    time.sleep(start_sleep)
    result = []
    for script in js:
        try:
            js_result = browser.execute_script(
                f"return {script}")
            result.append(js_result)
            if sleep_second != 0:
                time.sleep(sleep_second)
        except Exception as e:
            result.append(str(e))
    return result


def get_browser():
    """
    获取浏览器对象
    :return:
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("disable-cache")
    # return webdriver.Chrome(chrome_options=chrome_options)
    return webdriver.Chrome()

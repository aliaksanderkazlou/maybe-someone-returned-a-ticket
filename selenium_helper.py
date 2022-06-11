from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import config


def _get_random_user_agent():
    ua = UserAgent()
    return ua.random


def _get_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'user-agent={_get_random_user_agent()}')
    return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)


def try_to_find_element(driver, selector):
    try:
        return driver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None


def try_to_find_elements(driver, selector):
    try:
        return driver.find_elements(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None


def get_driver():
    driver = _get_chrome()

    driver.set_page_load_timeout(config['page_load_timeout'])
    driver.set_window_size(1920, 1080)

    return driver

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from fake_useragent import UserAgent

from config import config


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
    ua = UserAgent()
    user_agent = ua.random

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    driver.set_page_load_timeout(config['page_load_timeout'])

    return driver

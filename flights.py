import logging
from asyncio import sleep
from datetime import timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from config import config
from selenium_helper import get_driver, try_to_find_elements, try_to_find_element

logger = logging.getLogger(__name__)

date_table_mapping = {
    1: -3,
    2: -2,
    3: -1,
    4: 0,
    5: 1,
    6: 2,
    7: 3
}


def _wait_for_into_to_appear(driver):
    loader_css_selector = '.loader'

    WebDriverWait(driver, config['loading_short_timeout']).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, loader_css_selector)))
    WebDriverWait(driver, config['loading_long_timeout']).until_not(
        ec.presence_of_element_located((By.CSS_SELECTOR, loader_css_selector)))


def get_flights_search_url(destination, arrival, date, adults, children, infants):
    airline_url_prefix = config['airline_url_prefix']
    lang = config['lang']

    return f'{airline_url_prefix}' \
           f'&journey={destination}{arrival}{date}' \
           f'&adults={adults}&children={children}&infants={infants}&lang={lang}'


def get_available_flights_info(destination, arrival, date, adults, children, infants):
    flights = []

    url = get_flights_search_url(destination, arrival, date.strftime('%Y%m%d'), adults, children, infants)

    with get_driver() as driver:
        try:
            driver.get(url)

            waiting_time = 5000
            sleep(waiting_time)

            _wait_for_into_to_appear(driver)

            dates_table_css_selector = '.date-table li'

            dates_options = try_to_find_elements(driver, dates_table_css_selector)

            expected_dates_options_length = 7
            if len(dates_options) != expected_dates_options_length:
                raise Exception(f'Dates options count is not {expected_dates_options_length}')

            center_index = 4
            for date_option_index in range(0, expected_dates_options_length):
                date_option = dates_options[date_option_index]
                additional_classes = date_option.get_attribute("class").split()

                if 'disabled' not in additional_classes:
                    difference = date_option_index - center_index + 1
                    if difference > 0:
                        date_of_flight = date + timedelta(difference)
                    else:
                        date_of_flight = date - timedelta(difference * -1)

                    price = try_to_find_element(date_option, '.price .price-alternative .price-value')

                    flights.append({
                        'date_of_flight': date_of_flight,
                        'price': price.text
                    })

        except Exception as e:
            logger.exception(msg=f'{destination}-{arrival} {date} search failed...', exc_info=e)

    return flights

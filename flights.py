import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import config
from selenium_helper import get_driver, try_to_find_elements, try_to_find_element

logger = logging.getLogger(__name__)


def _get_flight_details(offer):
    time_of_departure_selector = '.itinerary-part-route .origin .time'
    time_or_arrival_selector = '.itinerary-part-route .destination .time'
    economy_cost_selector = '.cabin.economy .price .price-value'
    business_cost_selector = '.cabin.business .price .price-value'

    time_of_departure = try_to_find_element(offer, time_of_departure_selector).text
    time_of_arrival = try_to_find_element(offer, time_or_arrival_selector).text

    economy_cost = try_to_find_element(offer, economy_cost_selector)
    business_cost = try_to_find_element(offer, business_cost_selector)

    return {
        'time_of_departure': time_of_departure,
        'time_of_arrival': time_of_arrival,
        'economy_cost': economy_cost.text if economy_cost is not None else None,
        'business_cost': business_cost.text if business_cost is not None else None,
    }


def _wait_for_into_to_appear(driver):
    loader_css_selector = '.loader'

    WebDriverWait(driver, config['loading_short_timeout']).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, loader_css_selector)))
    WebDriverWait(driver, config['loading_long_timeout']).until_not(
        EC.presence_of_element_located((By.CSS_SELECTOR, loader_css_selector)))


def get_flights_search_url(destination, arrival, date, adults, children, infants):
    airline_url_prefix = config['airline_url_prefix']
    lang = config['lang']

    return f'{airline_url_prefix}' \
           f'&journey={destination}{arrival}{date}' \
           f'&adults={adults}&children={children}&infants={infants}&lang={lang}'


def get_available_flights_info(destination, arrival, date, adults, children, infants):
    flights = []

    url = get_flights_search_url(destination, arrival, date, adults, children, infants)

    with get_driver() as driver:
        try:
            driver.get(url)

            _wait_for_into_to_appear(driver)

            no_flights_css_selector = '.no-book-rows'
            offers_css_selector = '.offer-item'

            no_flights = try_to_find_element(driver, no_flights_css_selector)
            offers = try_to_find_elements(driver, offers_css_selector)

            if no_flights is None and len(offers) > 0:
                flights = [_get_flight_details(offer) for offer in offers]

        except Exception as e:
            logger.exception(msg=f'{destination}-{arrival} {date} search failed...', exc_info=e)

    return flights

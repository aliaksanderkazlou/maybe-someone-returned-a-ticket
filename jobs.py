from db import get_next_search, update_last_checked, get_search_subscription_info
from flights import get_available_flights_info


def _process_flight(flight, destination, arrival, date, adults, children, infants):
    update_last_checked(destination, arrival, date, adults, children, infants)

    search_subscription_info = get_search_subscription_info(destination, arrival, date, adults, children, infants)

    for info in search_subscription_info:
        chat_id = info[0]
        last_notified = info[1]



def start_job():
    next_search = get_next_search()

    destination = next_search[0]
    arrival = next_search[1]
    date = next_search[2]
    adults = next_search[3]
    children = next_search[4]
    infants = next_search[5]

    for available_flight in get_available_flights_info(
        destination,
        arrival,
        date,
        adults,
        children,
        infants):
        _process_flight(
            available_flight,
            destination,
            arrival,
            date,
            adults,
            children,
            infants)

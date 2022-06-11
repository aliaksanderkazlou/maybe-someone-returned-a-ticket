from db import get_next_search
from flights import get_available_flights_info


def start_job():
    next_search = get_next_search()

    destination = next_search[0]
    arrival = next_search[1]
    date = next_search[2].strftime('%Y%m%d')
    adults = next_search[3]
    children = next_search[4]
    infants = next_search[5]

    available_flights = get_available_flights_info(
        destination,
        arrival,
        date,
        adults,
        children,
        infants)

    print(available_flights)

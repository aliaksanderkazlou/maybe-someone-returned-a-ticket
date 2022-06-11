from datetime import datetime

import psycopg2

from config import config


def _connect_to_db():
    connection = psycopg2.connect(config['db_connection_string'])
    connection.autocommit = True

    return connection


def _create_searches_table(cursor):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {config['searches_table']}(
            id SERIAL PRIMARY KEY,
            user_id SERIAL NOT NULL,
            destination VARCHAR(3) NOT NULL,
            arrival VARCHAR(3) NOT NULL,
            date_of_flight DATE NOT NULL,
            adults NUMERIC NOT NULL,
            children NUMERIC NOT NULL,
            infants NUMERIC NOT NULL,
            last_checked TIMESTAMP,
            last_notified_user TIMESTAMP
        );""")

    cursor.execute(f"""
        CREATE UNIQUE INDEX IF NOT EXISTS ix_searches_table_unique ON {config['searches_table']}(
            user_id,
            destination,
            arrival,
            date_of_flight
        );""")


def _create_users_table(cursor):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {config['users_table']}(
            id SERIAL PRIMARY KEY,
            chat_id NUMERIC NOT NULL,
            first_name VARCHAR(45),
            last_name VARCHAR(45),
            same_flight_update_frequency NUMERIC NOT NULL
        );""")


def create_db_structure_if_not_exists():
    with _connect_to_db() as connection:
        with connection.cursor() as cursor:
            _create_users_table(cursor)
            _create_searches_table(cursor)


def create_user(chat_id, first_name, last_name):
    with _connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO {config['users_table']} (
                    chat_id,
                    first_name,
                    last_name,
                    same_flight_update_frequency)
                VALUES (%s, %s, %s, %s)""",
                (chat_id, first_name, last_name, int(config['same_flight_update_frequency'])))


def delete_user(chat_id):
    with _connect_to_db() as connection:
        with connection.cursor() as cursor:
            user_id = get_user_id_by_chat_id(chat_id)

            cursor.execute(f"""DELETE FROM {config['searches_table']} WHERE user_id = %s""", [user_id])
            cursor.execute(f"""DELETE FROM {config['users_table']} WHERE chat_id = %s""", [chat_id])


def get_chat_id_by_user_id(user_id):
    with _connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT chat_id FROM {config['users_table']} WHERE id = %s""", [user_id])

            return cursor.fetchone()[0]


def get_user_id_by_chat_id(chat_id):
    with _connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT id FROM {config['users_table']} WHERE chat_id = %s""", [chat_id])

            return cursor.fetchone()[0]


def create_search(destination, arrival, dates_range, user_id, adults, children, infants):
    with _connect_to_db() as connection:
        with connection.cursor() as cursor:
            for date_of_flight in dates_range:
                cursor.execute(
                    f"""
                    INSERT INTO {config['searches_table']} (
                        user_id,
                        destination,
                        arrival,
                        date_of_flight,
                        adults,
                        children,
                        infants)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (user_id, destination, arrival, date_of_flight, adults, children, infants))


def delete_search(destination, arrival, user_id):
    with _connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""DELETE FROM {config['searches_table']} WHERE destination = %s AND arrival = %s AND user_id = %s""",
                (destination, arrival, user_id))


def update_last_checked(destination, arrival, date_of_flight, adults, children, infants):
    with _connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE {config['searches_table']} 
                SET last_checked = %s
                WHERE destination = %s 
                    AND arrival = %s
                    AND date_of_flight = %s
                    AND adults = %s
                    AND children = %s
                    AND infants = %s""",
                (datetime.now(), destination, arrival, date_of_flight, adults, children, infants))


def get_search_subscription_info(destination, arrival, date_of_flight, adults, children, infants):
    with _connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT usr.chat_id, srh.last_notified_user FROM {config['searches_table']} srh
                    JOIN {config['users_table']} usr ON srh.user_id = usr.id
                WHERE srh.destination = %s 
                    AND srh.arrival = %s 
                    AND srh.date_of_flight = %s
                    AND srh.adults = %s
                    AND srh.children = %s
                    AND shr.infants = %s""",
                [destination, arrival, date_of_flight, adults, children, infants])

            return cursor.fetchall()


def get_next_search():
    with _connect_to_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT
                    destination,
                    arrival,
                    date_of_flight,
                    adults,
                    children,
                    infants
                FROM {config['searches_table']}
                ORDER BY last_checked ASC NULLS FIRST, destination, arrival
                LIMIT 1""")

            return cursor.fetchone()

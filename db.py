from pymongo import MongoClient

from config import config


def _get_database():
    connection_string = config['connection_string']
    client = MongoClient(connection_string)

    return client[config['db_name']]


def create_user(chat_id, first_name, last_name):
    with _get_database() as db:
        collection = db[config['users_collection']]

        collection.insert_one({
            'chat_id': chat_id,
            'first_name': first_name,
            'last_name': last_name,
            'same_flight_update_frequency': int(config['same_flight_update_frequency'])
        })


def delete_user(chat_id):
    with _get_database() as db:
        collection = db[config['users_collection']]

        collection.delete_one({'chat_id': chat_id})


def set_user_settings(chat_id, same_flight_update_frequency):
    with _get_database() as db:
        collection = db[config['users_collection']]

        collection.update_one(
            {'chat_id': chat_id},
            {'$set': {'same_flight_update_frequency': same_flight_update_frequency}}
        )


def create_search(destination, arrival, dates_range, user_id):
    with _get_database() as db:
        collection = db[config['searches_collection']]




def delete_search(destination, arrival, user_id):
    raise NotImplementedError


def update_last_checked(destination, arrival, date):
    raise NotImplementedError

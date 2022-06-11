from datetime import date, timedelta

from db import create_db_structure_if_not_exists, create_user, create_search, update_last_checked, \
    get_chat_id_by_user_id
from jobs import start_job

if __name__ == '__main__':
    create_db_structure_if_not_exists()

    start_job()


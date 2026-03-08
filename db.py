import os

import psycopg2


def inject_db_conn(func):
    def wrapper(*args, **kwargs):
        with psycopg2.connect(host="localhost", database=os.getenv('BANK_DB'), user=os.getenv('BANK_DB_USER'),
                                password=os.getenv('BANK_DB_PWD')) as conn:
            return func(conn, *args, **kwargs)
    return wrapper
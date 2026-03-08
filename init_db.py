import contextlib
import os
import random
import traceback
from datetime import timedelta, date, datetime
from multiprocessing import Pool
# from random import randint, randrange

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_values
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database, create_database
import models

from dateutil.relativedelta import relativedelta

load_dotenv()


@contextlib.contextmanager
def get_pg_conn():
    conn = None
    try:
        conn = psycopg2.connect(host="localhost", database=os.getenv('BANK_DB'), user=os.getenv('BANK_DB_USER'),
                                password=os.getenv('BANK_DB_PWD'))
        yield conn
    finally:
        if conn is not None:
            conn.close()


def run():
    while True:
        _choice = input("Mitä haluat tehdä ("
                        "\n0: lopeta"
                        "\n1: luo tietokanta"
                        "\n2: populoi event_typet"
                        "\n3: populoi accountit"
                        "\n4: populoi categoryt): ")
        if _choice == "0":
            break
        elif _choice == "1":
            _create_db_and_tables()
        elif _choice == "2":
            _populate_event_types()
        elif _choice == "3":
            _populate_accounts()
        elif _choice == "4":
            _populate_categories()
        elif _choice == "5":
            _populate_account_events()
        elif _choice == "6":
            _clean_account_events()
            _populate_account_events()


def _clean_account_events():
    with get_pg_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM account_events")
            conn.commit()



def _populate_month(args):
    import random
    fom, seconds_in_month, _account_id, num_of_events = args





    account_event_values = []

    for i in range(num_of_events):
        random_second = random.randrange(seconds_in_month)
        dt = fom + timedelta(seconds=random_second)
        print(f"############### {dt:%Y-%m-%d %H:%M:%S%z} - {_account_id} ###############")
        value = round(2 + 9998 * random.random(), 2)
        account_event_type = None
        if random.random() < 0.66:
            account_event_type = 1
        else:
            account_event_type = 2

        category = random.randint(1, 3)
        account_event_values.append(
            {'value': value, 'dt': dt, 'account_id': _account_id,'account_event_type_id': account_event_type, 'category_id': category})


    with get_pg_conn() as conn:
        with conn.cursor() as cur:
            try:
                execute_values(cur, "INSERT INTO account_events(value, dt, account_id, account_event_type_id, category_id) VALUES %s", account_event_values, template='(%(value)s, %(dt)s, %(account_id)s, %(account_event_type_id)s, %(category_id)s)')
                conn.commit()
            except Exception as e:
                conn.rollback()
                traceback.print_exc()



# Source - https://stackoverflow.com/a/30714165
# Posted by Eugene Yarmash, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-08, License - CC BY-SA 4.0

def _is_leap_year(year):
    """Determine whether a year is a leap year."""

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _populate_account_with_random_events(_account_id):
    _now = datetime.now()
    _start_date = _now - timedelta(days=365 * 3)
    tasks = []
    for month in range(3*12):
        _date = _start_date + relativedelta(months=month)

        num_of_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        dim = num_of_days[_date.month - 1]
        if _date.month - 1 == 1 and _is_leap_year(_date.year):
            dim = 29
        first_of_month = datetime(_date.year, _date.month, 1, hour=0, minute=0, second=0)

        seconds_in_month = dim * 24 * 60 * 60



        num_of_events = random.randint(50, 200)



        tasks.append((first_of_month, seconds_in_month, _account_id, num_of_events))




    with Pool(processes=4) as pool:
        print("#################ALKAA#######################")
        print(f"################# {tasks} ################")
        pool.map(_populate_month, tasks)



def _populate_account_events():
    for account_id in [1, 2]:
        _populate_account_with_random_events(account_id)


def _populate_categories():
    with get_pg_conn() as conn:
        with conn.cursor() as cur:
            _qry = "INSERT INTO categories(id, category) VALUES(%s, %s)"
            event_types = {1: 'Home', 2: 'Groceries', 3: 'Hobbies'}
            try:
                for key, value in event_types.items():
                    cur.execute(_qry, (key, value))
                conn.commit()
            except Exception as e:
                conn.rollback()
                traceback.print_exc()


def _populate_accounts():
    with get_pg_conn() as conn:
        with conn.cursor() as cur:
            _qry = "INSERT INTO accounts(id, account_number) VALUES(%s, %s)"
            event_types = {1: 'FI-12 2342 23405', 2: 'FI-12 5555 12345'}
            try:
                for key, value in event_types.items():
                    cur.execute(_qry, (key, value))
                conn.commit()
            except Exception as e:
                conn.rollback()
                traceback.print_exc()


def _populate_event_types():
    with get_pg_conn() as conn:
        with conn.cursor() as cur:
            _qry = "INSERT INTO account_event_types(id, event_type) VALUES(%s, %s)"
            event_types = {1: 'expense', 2: 'income'}
            try:
                for key, value in event_types.items():
                    cur.execute(_qry, (key, value))
                conn.commit()
            except Exception as e:
                conn.rollback()
                traceback.print_exc()


def _create_db_and_tables():
    dst_user = input("Anna tietokannan (Postgres) käyttäjän nimi (oletuksena postgres): ")
    dst_pwd = input("Anna tietokannan (Postgres) käyttäjän salasana:")
    dst_db = input(f"Anna tietokannan (Postgres) nimi:")
    dst_db_port = input("Anna tietokannan (Postgres) portti (oletuksena 5432): ")

    if dst_db_port == "":
        dst_db_port = "5432"

    if dst_user == "":
        dst_user = "postgres"

    dst_conn_str = f"postgresql+psycopg2://{dst_user}:{dst_pwd}@localhost:{dst_db_port}/{dst_db}"

    if database_exists(dst_conn_str):
        drop_database(dst_conn_str)
    create_database(dst_conn_str)

    engine = create_engine(dst_conn_str)
    if hasattr(models, 'Base'):
        _metadata = models.Base.metadata
    elif hasattr(models, 'metadata'):
        _metadata = models.metadata
    else:
        raise Exception('metadata missing')

    _metadata.create_all(engine)


if __name__ == '__main__':
    run()

from psycopg2.extras import DictCursor, RealDictCursor

from repositories.AccountsRepository import AccountsRepository
from services.ABCAccountsService import ABCAccountsService


class AccountsPgRepository(AccountsRepository):

    def __init__(self, conn):
        self.conn = conn

    def get_all(self):
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM accounts')
            return cursor.fetchall()

    def get_events_by_account_and_year(self, account_id: int, year: int):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT account_number, "
                           "ROUND(AVG(value)::numeric,2)::float AS value, "
                           "EXTRACT(MONTH FROM dt) AS month "
                           "FROM account_events AS ae "
                           "INNER JOIN accounts AS a ON a.id = ae.account_id "
                           "INNER JOIN categories AS c ON c.id = ae.category_id "
                           "INNER JOIN account_event_types AS aet ON aet.id = ae.account_event_type_id "
                           "WHERE a.id = %s "
                           "AND EXTRACT(YEAR FROM dt) = %s "
                           "AND aet.event_type = 'expense' "
                           "GROUP BY month, a.account_number "
                           "ORDER BY month ASC", (account_id, year))
            return cursor.fetchall()

    def get_events_by_account_year_and_month(self, account_id: int, year: int, month: int):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT account_number, "
                           "ROUND(AVG(value)::numeric,2) AS value, "
                           "EXTRACT(MONTH FROM dt) AS month, "
                           "EXTRACT(DAY FROM dt) AS day "
                           "FROM account_events AS ae "
                           "INNER JOIN accounts AS a ON a.id = ae.account_id "
                           "INNER JOIN categories AS c ON c.id = ae.category_id "
                           "INNER JOIN account_event_types AS aet ON aet.id = ae.account_event_type_id "
                           "WHERE a.id = %s "
                           "AND EXTRACT(YEAR FROM dt) = %s "
                           "AND EXTRACT(MONTH FROM dt) = %s "
                           "AND aet.event_type = 'expense' "
                           "GROUP BY month, day, a.account_number "
                           "ORDER BY month, day ASC", (account_id, year, month))
            return cursor.fetchall()

    def get_events_by_account_year_month_and_day(self, account_id: int, year: int, month: int, day: int):
        print(f"account_id: {account_id}, year: {year}, month: {month}, day: {day}")
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT a.account_number, "
                           "ROUND(AVG(value)::numeric,2) AS value,"
                           "EXTRACT(MONTH FROM dt) AS month,"
                           "EXTRACT(DAY FROM dt) AS day, "
                           "EXTRACT(HOUR FROM dt) AS hour "
                           "FROM account_events AS ae "
                           "INNER JOIN accounts AS a ON a.id = ae.account_id "
                           "INNER JOIN categories AS c ON c.id = ae.category_id "
                           "INNER JOIN account_event_types AS aet ON aet.id = ae.account_event_type_id "
                           "WHERE a.id = %s "
                           "AND EXTRACT(YEAR FROM dt) = %s "
                           "AND EXTRACT(MONTH FROM dt) = %s "
                           "AND EXTRACT (DAY FROM dt) = %s "
                           "AND aet.event_type = 'expense' "
                           "GROUP BY month, day, hour, a.account_number "
                           "ORDER BY month, day, hour ASC", (account_id, year, month, day))
            return cursor.fetchall()

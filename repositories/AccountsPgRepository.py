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
        pass

    def get_events_by_account_year_and_month(self, account_id: int, year: int, month: int):
        pass

    def get_events_by_account_year_month_and_day(self, account_id: int, year: int, month: int, day: int):
        pass
from repositories.AccountsRepository import AccountsRepository
from services.ABCAccountsService import ABCAccountsService


class AccountsPgRepository(AccountsRepository):

    def __init__(self, conn):
        self.conn = conn

    def get_all(self):
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM accounts')
            return cursor.fetchall()
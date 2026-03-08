from repositories.AccountsPgRepository import AccountsPgRepository
from repositories.AccountsRepository import AccountsRepository


def create_accounts_repository(conn):
    return AccountsPgRepository(conn)


def inject_accounts_repo(func):
    def wrapper(conn, *args, **kwargs):
        repo = create_accounts_repository(conn)
        return func(repo, *args, **kwargs)
    return wrapper
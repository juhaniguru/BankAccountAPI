from repositories.factories import create_accounts_repository
from services.AccountsService import AccountsService


def create_accounts_service(repository):

    service = AccountsService(repository)
    return service

def inject_accounts_service(func):
    def wrapper(repo, *args, **kwargs):
        service = create_accounts_service(repo)
        return func(service, *args, **kwargs)
    return wrapper
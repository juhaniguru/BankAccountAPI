import abc

from services.ABCAccountsService import ABCAccountsService


class AccountsRepository(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError()
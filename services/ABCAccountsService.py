import abc


class ABCAccountsService(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_events_by_account(self, account_id: int, dt: int, step: str):
        raise NotImplementedError()
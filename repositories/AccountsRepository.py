import abc




class AccountsRepository(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_events_by_account_and_year(self, account_id: int, year: int):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_events_by_account_year_and_month(self, account_id: int, year: int, month: int):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_events_by_account_year_month_and_day(self, account_id: int, year: int, month: int, day: int):        raise NotImplementedError()

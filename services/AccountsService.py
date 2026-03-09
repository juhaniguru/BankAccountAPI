import datetime

from services.ABCAccountsService import ABCAccountsService


class AccountsService(ABCAccountsService):


    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_events_by_account(self, account_id: int, dt: int, step: str):
        _date = datetime.datetime.fromtimestamp(int(dt))
        step = step.upper()
        events = []
        if step == "YEAR":
            events = self.repository.get_events_by_account_and_year(account_id, _date.year)
        elif step == "MONTH":
            events = self.repository.get_events_by_account_year_and_month(account_id, _date.year, _date.month)
        elif step == "DAY":
            events = self.repository.get_events_by_account_year_month_and_day(account_id, _date.year, _date.month, _date.day)
        else:
            raise Exception(f"Invalid step: {step}")
        return events

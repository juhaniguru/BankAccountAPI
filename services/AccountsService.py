import datetime

from services.ABCAccountsService import ABCAccountsService


class AccountsService(ABCAccountsService):

    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_events_by_account(self, account_id: int, dt: int, step: str):
        _date = datetime.datetime.fromtimestamp(int(dt) // 1000)
        step = step.upper()
        events = []
        if step == "YEAR":
            events = self.repository.get_events_by_account_and_year(account_id, _date.year)
            for i in range(len(events)):
                events[i]['date'] = datetime.datetime(int(_date.year), int(events[i]['month']), 1).isoformat()
        elif step == "MONTH":
            events = self.repository.get_events_by_account_year_and_month(account_id, _date.year, _date.month)
            for i in range(len(events)):
                events[i]['date'] = datetime.datetime(int(_date.year), int(events[i]['month']),
                                                      int(events[i]['day'])).isoformat()
        elif step == "DAY":
            events = self.repository.get_events_by_account_year_month_and_day(account_id, _date.year, _date.month,
                                                                              _date.day)

            events = self._fill_in_missing_hours(events, _date.year, _date.month, _date.day)
        else:
            raise Exception(f"Invalid step: {step}")
        return events

    def _fill_in_missing_hours(self, original_events, y, m, d):
        events = []
        for h in range(0, 24):
            events.append({
                'date': datetime.datetime(y, m, d, int(h)).isoformat(),
                'day': d,
                'month': m,
                'hour': h,
                'value': self._find_value_by_hour(h, original_events)

            })
        return events

    def _find_value_by_hour(self, hour, events):
        value = 0
        for event in events:
            if event['hour'] == hour:
                value = event['value']
                break

        return value

from flask import jsonify

from db import inject_db_conn
from repositories.factories import inject_accounts_repo
from services.ABCAccountsService import ABCAccountsService
from services.factories import inject_accounts_service


@inject_db_conn
@inject_accounts_repo
@inject_accounts_service
def get_all(service: ABCAccountsService):
    accounts = service.get_all()
    accounts_json = []
    for account in accounts:
        accounts_json.append({
            'id': account[0],
            'accountNumber': account[1],

        })

    return jsonify(accounts_json)

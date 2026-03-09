from dotenv import load_dotenv
from flask import Flask

import controllers.accounts

app = Flask(__name__)

load_dotenv()

app.add_url_rule('/api/v1/accounts', 'get_accounts', controllers.accounts.get_all, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

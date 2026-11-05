# -*- coding: utf-8 -*-
import sys
from flask_migrate import Migrate
from application import create_app
from application.extensions import db

app = create_app('production')
migrate = Migrate(app, db)

if __name__ == '__main__':
    if sys.argv[1:] == ['runserver']:
        app.run(host='127.0.0.1', port=7345, debug=False)
    else:
        app.cli.main(args=sys.argv[1:])

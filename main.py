#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''plik główny całej aplikacji'''

#importy modułów py
from flask import Flask

#importy nasze
from views import pages, login_manager
from models import db
from config import DB, APP

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB.PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DB.TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = APP.APP_KEY
app.register_blueprint(pages)

db.init_app(app)
login_manager.init_app(app)

if __name__ == '__main__':
    app.run(host=APP.IP, port=APP.PORT, debug=APP.DEBUG)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""plik główny całej aplikacji."""

# importy modułów py
from flask import Flask

# importy nasze
from views import pages
from views_admin import pages_admin
from views_login_system import pages_log_sys, login_manager
from mail_sending import mail
from db_models import db
from config import DB, APP, EMAIL

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB.PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DB.TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = APP.APP_KEY
app.config['MAIL_SERVER'] = EMAIL.SERVER
app.config['MAIL_PORT'] = EMAIL.PORT
app.config['MAIL_USE_SSL'] = EMAIL.SSL
app.config['MAIL_USERNAME'] = EMAIL.USERNAME
app.config['MAIL_PASSWORD'] = EMAIL.PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = EMAIL.DEFAULT_SENDER

app.register_blueprint(pages)
app.register_blueprint(pages_admin)
app.register_blueprint(pages_log_sys)
login_manager.init_app(app)
mail.init_app(app)
db.init_app(app)

if __name__ == '__main__':
    app.run(host=APP.IP, port=APP.PORT, debug=APP.DEBUG)

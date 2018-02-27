#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''plik główny całej aplikacji'''

#importy modułów py
from flask import Flask

#importy nasze
from views import pages, login_manager
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grave_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '\x88\xe7\xfa\x94\xbb\xa0s\xfa\xaf~\x03\xb7:\x9d\xe6I\x12\x07\\\x02yXU\xb6'
app.register_blueprint(pages)

db.init_app(app)
login_manager.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)

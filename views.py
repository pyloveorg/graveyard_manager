#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''plik zawierający funkcje renderowanych stron'''

#importy modułów py
import bcrypt
import uuid
import datetime
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from itsdangerous import URLSafeSerializer

#importy nasze
from validate import RegisterForm, LoginForm, ChangePwForm, ChangeDataForm
from models import db, User, Grave, Parcel, ParcelType, Family, Payments
from config import APP

pages = Blueprint('pages', __name__)
login_manager = LoginManager()
serializer = URLSafeSerializer(APP.APP_KEY)

@login_manager.user_loader
def load_user(session_token):
    '''wczytywanie uzytkownika przy pomocy tokena'''
    return User.query.filter_by(token_id=session_token).first()


@pages.route('/')
def index():
    '''renderowanie strony głównej'''
    return render_template('index.html')


@pages.route('/login', methods=['GET', 'POST'])
def login():
    '''strona logowania'''
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user_request = User.query.filter_by(email=form.email.data).first()
        if user_request:
            if bcrypt.checkpw(form.password.data.encode('UTF_8'), user_request.password):
                login_user(user_request)
                flash('Zostałeś poprawnie zalogowany!')
                return redirect(url_for('pages.index'))
        flash('Niepawidłowy e-mail lub hasło')
        return redirect(url_for('pages.login'))
    return render_template('login.html', form=form)


@pages.route('/logout')
@login_required
def logout():
    '''wylogowywanie użytkownika i przekierowywanie na stronę główną'''
    logout_user()
    return redirect(url_for('pages.index'))


@pages.route('/register', methods=['GET', 'POST'])
def register():
    '''strona rejestracji'''
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        unique_value = str(uuid.uuid4())
        new_user = User(email=form.email.data,
                        password=bcrypt.hashpw(form.password.data.encode('UTF_8'),
                                               bcrypt.gensalt()),
                        token_id=serializer.dumps([form.email.data, unique_value]),
                        name=form.name.data,
                        last_name=form.last_name.data,
                        city=form.city.data,
                        zip_code=form.zip_code.data,
                        street=form.street.data,
                        house_number=form.house_number.data,
                        flat_number=form.flat_number.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('pages.login'))
    return render_template('user_settings.html', form=form)


@pages.route('/user', methods=['POST', 'GET'])
@login_required
def user_page():
    '''ogólny panel ustawień użytkownika'''
    graves = Grave.query.filter_by(user_id=current_user.id)
    return render_template('user_page.html', graves=graves)


@pages.route('/user/password', methods=['POST', 'GET'])
@login_required
def user_set_pw():
    '''zmiana hasła użytkownika'''
    form = ChangePwForm(request.form)
    if request.method == 'POST' and form.validate():
        unique_value = str(uuid.uuid4())
        user = User.query.get(current_user.id)
        user.password = bcrypt.hashpw(form.password.data.encode('UTF_8'), bcrypt.gensalt())
        user.token_id = serializer.dumps([user.email, unique_value])
        db.session.commit()
        login_user(user)
        return redirect(url_for('pages.user_page'))
    return render_template('user_settings.html', form=form)


@pages.route('/user/data', methods=['POST', 'GET'])
@login_required
def user_set_data():
    '''zmiana danych personalnych użytkownika'''
    user = User.query.get(current_user.id)
    form = ChangeDataForm(request.form,
                          name=user.name,
                          last_name=user.last_name,
                          city=user.city,
                          zip_code=user.zip_code,
                          street=user.street,
                          house_number=user.house_number,
                          flat_number=user.flat_number)
    if request.method == 'POST' and form.validate():
        user.name = form.name.data
        user.last_name = form.last_name.data
        user.city = form.city.data
        user.zip_code = form.zip_code.data
        user.street = form.street.data
        user.house_number = form.house_number.data
        user.flat_number = form.flat_number.data
        db.session.commit()
        return redirect(url_for('pages.user_page'))
    return render_template('user_settings.html', form=form)


@pages.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    if current_user.admin:
        txt = 'cześć adminie'
        return txt
    return redirect(url_for('pages.index'))


@pages.route('/add_grave', methods=['POST', 'GET'])
def add_grave():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        birth_input = request.form['day_of_birth']
        day_of_birth = datetime.datetime.strptime(birth_input, '%Y-%m-%d')
        death_input = request.form['day_of_death']
        day_of_death = datetime.datetime.strptime(death_input, '%Y-%m-%d')
        parcel_id = 1
        new_grave = Grave(user_id=current_user.id,
                          parcel_id=parcel_id,
                          name=name,
                          last_name=last_name,
                          day_of_birth=day_of_birth,
                          day_of_death=day_of_death)
        db.session.add(new_grave)
        db.session.commit()
        return redirect(url_for('pages.user_page'))
    return render_template('add_grave.html')


@pages.app_errorhandler(401)
def page_unauthorized(e):
    '''obsługa erroru 401'''
    return redirect(url_for('pages.index'))


@pages.app_errorhandler(404)
def page_not_found(e):
    '''obsługa erroru 404'''
    return render_template('page_not_found.html')

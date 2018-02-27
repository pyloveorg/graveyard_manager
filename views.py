#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#importy modułów py
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import bcrypt

#importy nasze
from validate import RegisterForm, LoginForm
from models import db, User, Grave, Parcel, ParcelType, Family, Payments

pages = Blueprint('pages', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    form.email.default = 'aa'
    if request.method == 'POST' and form.validate():
        new_user = User(email=form.email.data,
                        password=bcrypt.hashpw(form.password.data.encode('UTF_8'), bcrypt.gensalt()),
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
    return render_template('register.html', form=form)


@pages.route('/user/settings')
@login_required
def user_settings():
    return 'settings :)'


@pages.app_errorhandler(401)
def page_unauthorized(e):
    return redirect(url_for('pages.index'))

@pages.app_errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html')

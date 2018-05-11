#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plik zawierający funkcje renderowanych stron."""

# importy modułów py
import datetime
import bcrypt
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import current_user, login_required, login_user
from sqlalchemy import func

# importy nasze
from data_validate import DataForm, PwForm, OldPwForm
from db_models import db, User, Grave, Parcel, ParcelType, Messages, Obituaries
from data_db_manage import change_user_data, change_user_pw

pages = Blueprint('pages', __name__)


@pages.route('/')
def index():
    """Renderowanie strony głównej."""
    messages_to_display = Messages.query.order_by(Messages.create_date.desc())
    return render_template('index.html', infos=messages_to_display)


@pages.route('/obituaries')
def obituaries():
    """Wyświatlanie nekrologów uporządkowane datami i tylko aktualne."""
    today_date = datetime.datetime.now() - datetime.timedelta(hours=4)
    obits = Obituaries.query.order_by(Obituaries.funeral_date.asc()).filter(
        Obituaries.funeral_date >= today_date)
    return render_template('obituaries.html', obits=obits)


@pages.route('/process', methods=['POST'])
def ajax_process():
    """Adres do komunikacji frontendu (ajax) z backendem (i bazą danych)."""
    email = request.form.get('email')
    email_in_db = User.query.filter_by(email=email).first()
    if email_in_db:
        return 'reserved'
    return 'none'


@pages.route('/user', methods=['POST', 'GET'])
@login_required
def user_page():
    """Ogólny panel ustawień użytkownika."""
    graves = Grave.query.filter_by(user_id=current_user.id)
    parcels = Parcel.query.all()
    max_p = db.session.query(func.max(Parcel.position_x)).scalar()
    return render_template('user_page.html', graves=graves, parcels=parcels, max_p=max_p)


@pages.route('/user/password', methods=['POST', 'GET'])
@login_required
def user_set_pw():
    """Zmiana hasła użytkownika."""
    form_pw = PwForm(request.form)
    form_oldpw = OldPwForm(request.form)
    user = User.query.get(current_user.id)
    if request.method == 'POST' and all([x.validate() for x in [form_pw, form_oldpw]]):
        if bcrypt.checkpw(form_oldpw.old_password.data.encode('UTF_8'), user.password):
            change_user_pw(user, form_pw)
            db.session.commit()
            # ponowne zalogowanie - zmiana tokena automatycznie wylogowuje
            login_user(user)
            flash('Hasło zostało prawidłowo zmienione!', 'succes')
            return redirect(url_for('pages.user_page'))
        flash('Podane hasło jest nieprawidłowe!', 'error')
        return redirect(url_for('pages.user_set_pw'))
    return render_template('user_settings.html', form_pw=form_pw, form_oldpw=form_oldpw)


@pages.route('/user/data', methods=['POST', 'GET'])
@login_required
def user_set_data():
    """Zmiana danych personalnych użytkownika."""
    user = User.query.get(current_user.id)
    form_oldpw = OldPwForm(request.form)
    form_data = DataForm(request.form,
                         name=user.name,
                         last_name=user.last_name,
                         city=user.city,
                         zip_code=user.zip_code,
                         street=user.street,
                         house_number=user.house_number,
                         flat_number=user.flat_number)
    if request.method == 'POST' and all([x.validate() for x in [form_oldpw, form_data]]):
        if bcrypt.checkpw(form_oldpw.old_password.data.encode('UTF_8'),
                          User.query.get(current_user.id).password):
            # zmiana danych użytkownika - funkcja importowana z data_db_manage
            change_user_data(user, form_data)
            db.session.commit()
            flash('Dane zostały prawidłowo zmodyfikowane!', 'succes')
        else:
            flash('Podane hasło jest nieprawidłowe!', 'error')
            return redirect(url_for('pages.user_set_data'))
        return redirect(url_for('pages.user_page'))
    return render_template('user_settings.html', form_oldpw=form_oldpw, form_data=form_data)


@pages.route('/add_grave/<p_id>', methods=['POST', 'GET'])
def add_grave(p_id):
    parcel = Parcel.query.filter_by(id=p_id).scalar()
    p_id = parcel.id
    if Grave.query.filter_by(parcel_id=p_id).first() is None:
        if request.method == 'POST':
            name = request.form['name']
            last_name = request.form['last_name']
            day_of_birth = datetime.datetime.strptime(request.form['day_of_birth'], '%Y-%m-%d')
            day_of_death = datetime.datetime.strptime(request.form['day_of_death'], '%Y-%m-%d')
            new_grave = Grave(user_id=current_user.id,
                              parcel_id=p_id,
                              name=name,
                              last_name=last_name,
                              day_of_birth=day_of_birth,
                              day_of_death=day_of_death)
            db.session.add(new_grave)
            db.session.commit()
            return redirect(url_for('pages.user_page'))
        return render_template('add_grave.html', p_id=p_id, parcel=parcel)
    else:
        flash('Ta parcela jest już zajęta', 'error')
        return redirect(url_for('pages.user_page'))


@pages.route('/grave/<grave_id>', methods=['POST', 'GET'])
def grave(grave_id):
    grave = Grave.query.filter_by(id=grave_id).first()
    parcel_grave = Parcel.query.filter_by(id=grave.parcel_id).first()
    parcel_type = ParcelType.query.filter_by(id=parcel_grave.parcel_type_id).first()

    if request.method == 'POST':
        grave.name = request.form['edited_name']
        grave.last_name = request.form['edited_last_name']
        grave.day_of_birth = datetime.datetime.strptime(request.form['edited_birth'], '%Y-%m-%d')
        grave.day_of_death = datetime.datetime.strptime(request.form['edited_death'], '%Y-%m-%d')
        db.session.commit()
    return render_template('grave_page.html', grave_id=grave_id, grave=grave, parcel_type=parcel_type)


@pages.route('/delete/<grave_id>', methods=['POST'])
def delete_grave(grave_id):
    grave = Grave.query.filter_by(id=grave_id).first()
    db.session.delete(grave)
    db.session.commit()
    return redirect(url_for('pages.user_page'))


@pages.app_errorhandler(404)
def page_not_found(e):
    """Obsługa erroru 404."""
    return render_template('page_404.html')

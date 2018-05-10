#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Obsługa powtarzalnych czynności z bazą danych i procesów z tym związanych."""

# importy modułów py
import uuid
import bcrypt
from itsdangerous import URLSafeSerializer

# importy nasze
from config import APP
from data_func_manage import convert_date
from models import User


serializer = URLSafeSerializer(APP.APP_KEY)


def register_new_user(form_email, form_pw, form_data):
    """Funkcja rejestrująca nowego użytkownika, parametry funkcji z wtforms."""
    unique_value = str(uuid.uuid4())
    new_user = User(email=form_email.email.data,
                    password=bcrypt.hashpw(form_pw.password.data.encode('UTF_8'), bcrypt.gensalt()),
                    token_id=serializer.dumps([form_email.email.data, unique_value]),
                    name=form_data.name.data,
                    last_name=form_data.last_name.data,
                    city=form_data.city.data,
                    zip_code=form_data.zip_code.data,
                    street=form_data.street.data,
                    house_number=form_data.house_number.data,
                    flat_number=form_data.flat_number.data)
    return new_user


def change_user_pw(user, form_pw, form=True):
    """Zmiana hasła użytkownika.

    form=True oznacza dane brane z wtforms, w innym przypadku form_pw to nowe hasło.
    """
    pw = form_pw.password.data if form else form_pw
    unique_value = str(uuid.uuid4())
    user.password = bcrypt.hashpw(pw.encode('UTF_8'), bcrypt.gensalt())
    user.token_id = serializer.dumps([user.email, unique_value])


def change_user_data(user, form_data):
    """Zmiana danych użytkownika, parametr form_data z wtforms."""
    user.name = form_data.name.data
    user.last_name = form_data.last_name.data
    user.city = form_data.city.data
    user.zip_code = form_data.zip_code.data
    user.street = form_data.street.data
    user.house_number = form_data.house_number.data
    user.flat_number = form_data.flat_number.data


def obituary_add_data(obituary_form, funeral_time):
    name = obituary_form.name.data
    surname = obituary_form.surname.data
    years_old = obituary_form.years_old.data
    death_date = convert_date(obituary_form.death_date.data)
    funeral_date = convert_date(obituary_form.funeral_date.data, funeral_time)
    gender = obituary_form.gender.data

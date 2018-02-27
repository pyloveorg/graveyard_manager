#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''plik do walidacji danych'''
#importy modułów py
from wtforms import Form, StringField, PasswordField
from wtforms.validators import ValidationError, input_required, email, length, equal_to
import re

#importy nasze
from models import db, User


def zip_code_validator(form, field):
    '''walidacja kodu pocztowego zgodnie ze standarem polskim "dd-ddd" '''
    if field.data != '':
        if not re.match(r'^\d\d-\d\d\d$', field.data):
            raise ValidationError('Niepoprawny kod pocztowy!')


def email_in_db(form, field):
    '''sprawdzanie czy adres email nie jest już w bazie'''
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Adres E-mail jest już w użyciu!')


def digit_or_none(form, field):
    '''pole musi pozostac puste lub być liczbą'''
    if field.data != '':
        if not field.data.isdigit():
            raise ValidationError('Niepoprawny numer!')


class RegisterForm(Form):
    email = StringField('Adres e-mail:',
                        [input_required(message='Pole wymagane!'),
                         email(message='Niepoprawny adres e-mail!'),
                         email_in_db,
                         length(max=63, message='Adres e-mail przekracza 63 znaki!')])
    password = PasswordField('Hasło:',
                             [input_required(message='Pole wymagane!'),
                              length(max=72, message='Hasło nie może być dłuższe niż 72 znaki!'),
                              equal_to('repeat_password', message = 'Hasła nie są identyczne!')])
    repeat_password = PasswordField('Powtórz hasło:')
    name = StringField('Imię:', [length(max=80)])
    last_name = StringField('Nazwisko:', [length(max=120)])
    city = StringField('Miasto:', [length(max=80)])
    zip_code = StringField('Kod pocztowy:', [zip_code_validator])
    street = StringField('Ulica:', [length(max=150)])
    house_number = StringField('Numer domu:', [digit_or_none])
    flat_number = StringField('Numer mieszkania:', [digit_or_none])

class LoginForm(Form):
    email = StringField('Adres e-mail', [input_required(message='Pole wymagane!')])
    password = PasswordField('Hasło', [input_required(message='Pole wymagane!')])

class SettingsForm(RegisterForm):
    email.default = 'abc'
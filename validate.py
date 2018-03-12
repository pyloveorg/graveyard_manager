#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''plik do walidacji danych'''
#importy modułów py
import re
from wtforms import Form, StringField, PasswordField
from wtforms.validators import ValidationError, input_required, email, length, equal_to


class PwForm(Form):
    '''klasa wtforms do ustalania hasła użytkownika'''
    password = PasswordField('Hasło:',
                             [input_required(message='Pole wymagane!'),
                              length(max=72, message='Hasło nie może być dłuższe niż 72 znaki!'),
                              equal_to('repeat_password', message='Hasła nie są identyczne!')])
    repeat_password = PasswordField('Powtórz hasło:')


class OldPwForm(Form):
    '''klasa wtforms do weryfikacji aktualnego hasła'''
    old_password = PasswordField('Aktualne hasło:', [input_required(message='Pole wymagane!')])


class DataForm(Form):
    '''klasa wtforms do ustawiania danych personalnych użytkownika'''
    def digit_or_none(self, field):
        '''pole musi pozostac puste lub być liczbą'''
        if field.data != '':
            if not field.data.isdigit():
                raise ValidationError('Niepoprawny numer!')

    def zip_code_validator(self, field):
        '''walidacja kodu pocztowego zgodnie ze standarem polskim "dd-ddd" '''
        if field.data != '':
            if not re.match(r'^\d\d-\d\d\d$', field.data):
                raise ValidationError('Niepoprawny kod pocztowy!')

    name = StringField('Imię:', [length(max=80)])
    last_name = StringField('Nazwisko:', [length(max=120)])
    city = StringField('Miasto:', [length(max=80)])
    zip_code = StringField('Kod pocztowy:', [zip_code_validator])
    street = StringField('Ulica:', [length(max=150)])
    house_number = StringField('Numer domu:', [digit_or_none])
    flat_number = StringField('Numer mieszkania:', [digit_or_none])


class EmailForm(Form):
    '''klasa wtforms do rejestracji użytkownika - ustawianie adresu e-mail'''
    email = StringField('Adres e-mail:',
                        [input_required(message='Pole wymagane!'),
                         email(message='Niepoprawny adres e-mail!'),
                         length(max=63, message='Adres e-mail przekracza 63 znaki!')])


class LoginForm(Form):
    '''klasa wtforms do logowania'''
    email = StringField('Adres e-mail', [input_required(message='Pole wymagane!')])
    password = PasswordField('Hasło', [input_required(message='Pole wymagane!')])

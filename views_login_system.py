#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plik zawierający funkcje dla systemu logowania/rejestracji."""

# importy modułów py
import bcrypt
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

# importy nasze
from config import APP
from data_validate import EmailForm, LoginForm, DataForm, PwForm, is_safe_next
from data_db_manage import register_new_user, change_user_data, change_user_pw
from data_func_manage import generate_password
from db_models import db, User
from mail_sending import common_msg

pages_log_sys = Blueprint('pages_log_sys', __name__)
login_manager = LoginManager()
temp_serializer = URLSafeTimedSerializer(APP.APP_KEY)


@login_manager.user_loader
def load_user(session_token):
    """Wczytywanie uzytkownika przy pomocy tokena."""
    return User.query.filter_by(token_id=session_token).first()


@login_manager.unauthorized_handler
def handle_needs_login():
    """Obsługa erroru 401.

    Przekierowanie do strony logowania, oraz przekazanie parametru next
    po zalogowaniu powrót na stronę żądaną.
    """
    flash('Musisz się najpierw zalogować!', 'error')
    return redirect(url_for('pages_log_sys.login', next=request.path))


@pages_log_sys.route('/login', methods=['GET', 'POST'])
def login():
    """Strona logowania."""
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))
    next_page = request.args.get('next')
    form_login = LoginForm(request.form)
    if request.method == 'POST' and form_login.validate():
        user_request = User.query.filter_by(email=form_login.email_login.data).first()
        if user_request and user_request.active_user:
            if bcrypt.checkpw(form_login.password.data.encode('UTF_8'), user_request.password):
                login_user(user_request)
                flash('Zostałeś poprawnie zalogowany!', 'succes')
                # sprawdza czy adres url + query string nie były zmodyfikowane
                return (redirect(next_page) if next_page and is_safe_next(next_page) else
                        redirect(url_for('pages.index')))
        flash('Niepawidłowy e-mail lub hasło!', 'error')
        return redirect(url_for('pages_log_sys.login'))
    return render_template('login.html', form_login=form_login)


@pages_log_sys.route('/pw_recovery', methods=['POST', 'GET'])
def password_recovery():
    """Strona do odzyskiwania hasła.

    Wymaga podania jedynie adresu email, dalsze instrukcje zostają wysłane na podany adres.
    """
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))
    form_email = EmailForm(request.form)
    if request.method == 'POST' and form_email.validate():
        user = User.query.filter_by(email=form_email.email.data).first()
        # sprawdzenie czy użytkownik jest w bazie oraz czy został aktywowany
        if user and user.active_user:
            password_token = temp_serializer.dumps(user.token_id, salt='pw-recovery')
            link_url = url_for('pages_log_sys.recovery_password',
                               pw_token=password_token,
                               _external=True)
            common_msg('Odzyskiwanie hasła', user.email, 'pw_recovery', link_url)
            flash('Na podany adres email zostały wysłane dalsze informacje.', 'succes')
            return redirect(url_for('pages.index'))
        flash('Podany adres e-mail nie istnieje!', 'error')
    return render_template('recovery.html', form_email=form_email)


@pages_log_sys.route('/pw_recovery/<pw_token>')
def recovery_password(pw_token):
    """Strona do generowania nowego hasła.

    Jest wysyłana drogą mailową w postaci url, po wejściu hasło zostaje
    zresetowane a następnie wysłane drugim mailem do użytkownika.
    """
    try:
        token_id = temp_serializer.loads(pw_token, salt='pw-recovery', max_age=3600)
        user = User.query.filter_by(token_id=token_id).first()
        # funkcja generująca hasło z modułu data_func_manage
        new_pw = generate_password()
        change_user_pw(user, new_pw, form=False)
        db.session.commit()
        common_msg('Nowe hasło', user.email, 'new_password', new_pw)
        flash('Nowe hasło zostało wysłane na twój e-mail.', 'succes')
        return redirect(url_for('pages_log_sys.login'))
    # wyjątek gdy link jest zmodyfikowany, wykorzystany lub przestarzały
    except (SignatureExpired, BadSignature, AttributeError):
        flash('Podany link jest nieaktywny!', 'error')
        return redirect(url_for('pages.index'))


@pages_log_sys.route('/logout')
@login_required
def logout():
    """Wylogowywanie użytkownika i przekierowywanie na stronę główną."""
    logout_user()
    flash('Zostałeś poprawnie wylogowany!', 'succes')
    return redirect(url_for('pages.index'))


@pages_log_sys.route('/register', methods=['GET', 'POST'])
def register():
    """Strona rejestracji."""
    if current_user.is_authenticated:
        return redirect(url_for('pages.index'))
    form_email = EmailForm(request.form)
    form_pw = PwForm(request.form)
    form_data = DataForm(request.form)
    if request.method == 'POST' and all([x.validate() for x in [form_email, form_pw, form_data]]):
        user = User.query.filter_by(email=form_email.email.data).first()
        if not user:
            # rejestracja nowego użytkownika
            new_user = register_new_user(form_email, form_pw, form_data)
            db.session.add(new_user)
            db.session.commit()
        elif not user.active_user:
            # zmiana danych użytkownika
            change_user_pw(user, form_pw)
            change_user_data(user, form_data)
            db.session.commit()
        else:
            flash('Podany adres e-mail jest w użyciu!', 'error')
            return redirect(url_for('pages_log_sys.register'))
        # wysyłanie e-maila z linkiem do aktywacji
        register_token = temp_serializer.dumps(form_email.email.data, salt='confirm-email')
        link_url = url_for('pages_log_sys.confirm_email', register_token=register_token,
                           _external=True)
        common_msg('Aktywacja konta', form_email.email.data, 'register_message', link_url)
        flash('Na podany adres email został wysłany kod weryfikacyjny!', 'succes')
        return redirect(url_for('pages.index'))
    return render_template('user_settings.html',
                           form_email=form_email,
                           form_pw=form_pw,
                           form_data=form_data)


@pages_log_sys.route('/confirm_email/<register_token>')
def confirm_email(register_token):
    """Strona do potwierdzania adresu e-mail.

    Jest generowana i wysyłana drogą mailową w postaci url, po wejściu status "active_user" zostaje
    zmieniony z domyślnego False na True co umożliwia zalogowanie.
    """
    try:
        email = temp_serializer.loads(register_token, salt='confirm-email', max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user.active_user:
            flash('Konto już jest aktywne!', 'error')
            return redirect(url_for('pages.index'))
        user.active_user = True
        db.session.commit()
        flash('Konto zostało aktywowane pomyślnie!', 'succes')
        return redirect(url_for('pages_log_sys.login'))
    except (SignatureExpired, BadSignature):
        flash('Podany link jest nieaktywny!', 'error')
        return redirect(url_for('pages.index'))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plik zawierający funkcje renderowanych stron dla administratora."""

from flask import Blueprint, redirect, url_for, render_template, request, flash, abort
from flask_login import current_user, login_required
import datetime

from models import db, Messages, Comments
from data_handling import add_new_post

pages_admin = Blueprint('pages_admin', __name__)


def admin_required(func):
    """Dekorator, sprawdza czy użytkownik ma status administratora."""
    def wrapper(*args, **kwargs):
        if current_user.admin:
            return func(*args, **kwargs)
        return abort(404)
    # musi być zmieniona nazwa - wynika to z samego flaska a nie konstrukcji dekoratora
    wrapper.__name__ = func.__name__
    return wrapper


@pages_admin.route('/admin', methods=['POST', 'GET'])
@login_required
@admin_required
def admin():
    """Panel administratora - wymaga statusu w bazie "admin=True"."""
    if request.method == 'POST':
        # parametry dodania nowego posta
        post_title = request.form.get('post_header', False)
        post_content = request.form.get('post_content', False)
        if post_title and post_content:
            # funkcja w data_handling
            new_message = add_new_post(post_title, post_content, datetime.datetime.now())
            db.session.add(new_message)
            db.session.commit()
            flash('Dodawanie wiadomości zakończone powodzeniem!', 'succes')
        else:
            flash('Nieprawidłowe dane', 'error')
        return redirect(url_for('pages_admin.admin'))
    return render_template('admin_page.html')


@pages_admin.route('/message/<message_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def message_edit(message_id):
    message = Messages.query.get_or_404(message_id)
    if request.method == 'POST':
        post_title = request.form.get('post_header', False)
        post_content = request.form.get('post_content', False)
        if post_title and post_content:
            message.title = post_title
            message.content = post_content
            db.session.commit()
            flash('Wiadomość zmodyfikowano pomyślnie!', 'succes')
        else:
            flash('Nieprawidłowe dane', 'error')
        return redirect(url_for('pages.index'))
    return render_template('message_edit.html', message=message)

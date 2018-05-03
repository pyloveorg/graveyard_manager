#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plik zawierający funkcje renderowanych stron dla administratora."""

from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_required

pages_admin = Blueprint('pages_admin', __name__)


def admin_required(func):
    """Dekorator, sprawdza czy użytkownik ma status administratora."""
    def wrapper(*args, **kwargs):
        if current_user.admin:
            return func(*args, **kwargs)
        return redirect(url_for('pages.index'))
    # musi być zmieniona nazwa - wynika to z samego flaska a nie konstrukcji dekoratora
    wrapper.__name__ = func.__name__
    return wrapper


@pages_admin.route('/admin', methods=['POST', 'GET'])
@login_required
@admin_required
def admin():
    """Panel administratora - wymaga statusu w bazie "admin=True"."""
    return render_template('admin_page.html')

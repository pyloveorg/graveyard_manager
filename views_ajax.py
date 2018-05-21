#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plik zawierający funkcje stron do kontaktu z ajaxem."""
# importy modułów py
from flask import request, Blueprint

# importy nasze
from db_models import User

pages_ajax = Blueprint('pages_ajax', __name__)


@pages_ajax.route('/ajax_email', methods=['POST'])
def ajax_email():
    """Adres do komunikacji frontendu (ajax) z backendem (i bazą danych)."""
    email = request.form.get('email')
    email_in_db = User.query.filter_by(email=email).first()
    if email_in_db:
        return 'reserved'
    return 'none'

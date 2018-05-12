#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plik zawierający funkcje renderowanych stron dostępnych bez zalogowania."""

# importy modułów py
import datetime
from flask import render_template, redirect, url_for, Blueprint

# importy nasze
from db_models import Messages, Obituaries

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


@pages.app_errorhandler(404)
def page_not_found(e):
    """Obsługa erroru 404."""
    return render_template('page_404.html')


@pages.app_errorhandler(405)
def page_wrong_method(e):
    """Obsługa erroru 405."""
    return redirect(url_for('pages.index'))

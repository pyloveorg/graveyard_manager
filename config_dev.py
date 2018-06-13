#!usr/bin/env python3
"""Plik konfiguracyjny deweloperski."""
import sys

class CONFIG_DB:
    """Konfiguracja bazy danych."""

    PATH = 'sqlite:///grave_db.db'
    TRACK_MODIFICATIONS = False
    DEFAULT_ACTIVE_USER = False


class CONFIG_APP:
    """Konfiguracja aplikacji."""

    IP = '127.0.0.1'
    PORT = 5000
    DEBUG = True
    APP_KEY = '\x88\xe7\xfa\x94\xbb\xa0s\xfa\xaf~\x03\xb7:\x9d\xe6I\x12\x07\\\x02yXU\xb6'


class CONFIG_EMAIL:
    """Konfiguracja serwera poczty."""

    SERVER = 'poczta.o2.pl'
    PORT = 465
    SSL = True
    USERNAME = 'graveyard_manager'
    PASSWORD = '@T15x?q7'
    DEFAULT_SENDER = 'graveyard_manager@o2.pl'
    FILES_PATH = 'static\\emails\\' if sys.platform == 'win32' else 'static/emails/'

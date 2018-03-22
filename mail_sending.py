#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Moduł do obsługi wysyłania e-maili."""
from flask_mail import Mail, Message

mail = Mail()


def common_msg(title, send_to, filename, *args):
    """Prosta funkcja do wysyłania e-maila.

    title = tytuł wiadomości,
    send_to = adresat,
    filename = nazwa pliku w folderze static/emails,
    *args - parametry dodawane do formatki
    """
    msg = Message(title, recipients=[send_to])
    with open('static/emails/{}'.format(filename), 'r') as file:
        message = file.read().format(*args)
    msg.body = message
    mail.send(msg)

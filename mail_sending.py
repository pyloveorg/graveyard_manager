#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Moduł do obsługi wysyłania e-maili."""
from flask_mail import Mail, Message
from config import EMAIL

mail = Mail()


def common_msg(title, send_to, filename, *args):
    """Prosta funkcja do wysyłania e-maila.

    title = tytuł wiadomości,
    send_to = adresat,
    filename = nazwa pliku w folderze static/emails,
    *args - parametry dodawane do formatki
    """
    msg = Message(title, recipients=[send_to])
    with open('{}{}'.format(EMAIL.FILES_PATH, filename), 'r') as file:
        message = file.read().format(*args)
    msg.body = message
    mail.send(msg)


def msg_to_all_users(subject, message, users):
    """Wiadomość wysyłana do wszystkich aktywnych użytkowników."""
    with mail.connect() as conn:
        for user in users:
            message = message
            subject = subject
            msg = Message(recipients=[user.email],
                          body=message,
                          subject=subject)
            conn.send(msg)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''moduł do obsługi wysyłania e-maili'''
from flask_mail import Mail, Message

mail = Mail()

def common_msg(title, send_to, filename, output):
    '''prosta funkcja do wysyłania e-maila, title = tytuł wiadomości, send_to = adresat,
    filename = nazwa pliku w folderze static/emails, output = zmienna dodawana do formatki'''
    msg = Message(title, recipients=[send_to])
    with open('static/emails/{}'.format(filename), 'r') as file:
        message = file.read().format(output)
    msg.body = message
    mail.send(msg)

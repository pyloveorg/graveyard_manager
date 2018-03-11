#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_mail import Mail, Message

mail = Mail()

def common_msg(title, send_to, filename, output):
    msg = Message(title, recipients=[send_to])
    with open('static/emails/{}'.format(filename), 'r') as file:
        message = file.read().format(output)
    msg.body = message
    mail.send(msg)

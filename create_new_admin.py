#!usr/bin/env python3
# -*- coding: utf-8 -*-
'''plik do tworzenia nowego konta administratora'''
import uuid
import bcrypt
from itsdangerous import URLSafeSerializer
from models import User
from main import db, app
from config import APP

app.app_context().push()
serializer = URLSafeSerializer(APP.APP_KEY)

admin_email = input('podaj email: ')
admin_pw = input('podaj hasło: ')
admin_pw_rep = input('powtórz hasło: ')

if admin_pw == admin_pw_rep:
    if not User.query.filter_by(email=admin_email).first():
        new_admin = User(email=admin_email,
                         active_user=True,
                         password=bcrypt.hashpw(admin_pw.encode('UTF_8'),
                                                bcrypt.gensalt()),
                         token_id=serializer.dumps([admin_email, str(uuid.uuid4())]),
                         admin=True)
        db.session.add(new_admin)
        db.session.commit()
        print('utworzono nowego administratora :)')
    else:
        print('taki e-mail jest już w użyciu :(')
else:
    print('hasła nie są identyczne...')

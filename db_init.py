# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Utworzenie pliku bazy danych.

Uwaga - tylko do jednokrotnego użycia gdy baza danych nie istnieje!!!
"""

# importy nasze
from main import app, db
from models import Parcel, ParcelType

# importy modułów py
from sqlalchemy import event
import numpy as np
import itertools

app.app_context().push()
db.create_all()
print('utworzono bazę danych')

print('tworzenie danych dodatkowych')
@event.listens_for(Parcel.__table__, 'after_create')
def insert_initial_coordinates(max_p):
    """Funkcja generująca koordynaty dla cmentarza o wymiarach 1 x max_p."""
    xvalues = np.arange(1, max_p + 1, 1)
    yvalues = np.arange(1, max_p + 1, 1)
    coordinates = list(itertools.product(xvalues, yvalues))

    for pair in coordinates:
        if (int(pair[1]) == 1) or \
                (int(pair[0]) in np.arange(1, ((1 + max_p) * max_p), max_p)) or \
                (int(pair[0]) in np.arange(max_p, max_p * max_p, max_p)) or \
                (int(pair[1]) == max_p + 1):
            new_parcel = Parcel(parcel_type_id=1,
                                position_x=int(pair[0]),
                                position_y=int(pair[1]))
        else:
            new_parcel = Parcel(parcel_type_id=2,
                                position_x=int(pair[0]),
                                position_y=int(pair[1]))
        db.session.add(new_parcel)
        db.session.commit()


@event.listens_for(ParcelType.__table__, 'after_create')
def insert_initial_types():
    """Funkcja tworząca dwa typy parceli."""
    border_type = ParcelType(price=150,
                             description='Border position')
    inner_type = ParcelType(price=100,
                            description='Inner position')
    db.session.add(border_type)
    db.session.add(inner_type)
    db.session.commit()


insert_initial_coordinates(10)
insert_initial_types()
print('zakonczono cały proces :)')

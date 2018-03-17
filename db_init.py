#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Utworzenie pliku bazy danych.

Uwaga - tylko do jednokrotnego użycia gdy baza danych nie istnieje!!!
"""
from main import app, db
app.app_context().push()
db.create_all()
print('utworzono bazę danych')

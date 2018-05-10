#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Moduł do generowania lub edytowania potrzebnych danych."""
import datetime
import random
import re


def generate_password():
    """Funkcja do generowania nowego hasła w przypadku utraty poprzedniego."""
    big_letters = [chr(x) for x in range(ord('A'), ord('Z')+1)]
    low_letters = [chr(x) for x in range(ord('a'), ord('z')+1)]
    numbers = [str(x) for x in range(0, 10)]
    special = ['!', '@', '#', '$', '%', '^', '&', '*', '?', '+']
    gen_pw = []
    for i in [random.sample(x, 2) for x in [big_letters, low_letters, numbers, special]]:
        gen_pw += i
    random.shuffle(gen_pw)
    return ''.join(gen_pw)


def convert_date(calendar_date, clock_time='0:0'):
    """Konwerter daty między html a py.

    Przyjmuje datę HTML w domyślnym formacie YYYY-MM-DD oraz opcjonalnie godzinę HH:MM i konwertuje
    na format czasu pythona
    """
    return (datetime.datetime.strptime(calendar_date, '%Y-%m-%d') +
            datetime.timedelta(hours=datetime.datetime.strptime(clock_time, '%H:%M').hour,
                               minutes=datetime.datetime.strptime(clock_time, '%H:%M').minute))

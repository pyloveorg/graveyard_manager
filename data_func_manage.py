#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Moduł do generowania lub edytowania potrzebnych danych."""
import datetime


def convert_date(calendar_date, clock_time='0:0', calendar_is_html=True, clock_is_str=True):
    """Konwerter daty między html a py.

    Przyjmuje datę HTML w domyślnym formacie YYYY-MM-DD oraz opcjonalnie godzinę HH:MM i konwertuje
    na format czasu pythona.
    Dopuszcza się zamiast daty i godziny w formie str podać w formacie pythonowej daty.
    """
    if calendar_is_html:
        calendar_date = datetime.datetime.strptime(calendar_date, '%Y-%m-%d')
    if clock_is_str:
        clock_time = datetime.datetime.strptime(clock_time, '%H:%M')
    return calendar_date + datetime.timedelta(hours=clock_time.hour, minutes=clock_time.minute)

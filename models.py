#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active_user = db.Column(db.Boolean, default=True)
    token_id = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(63), unique=True, nullable=False)
    password = db.Column(db.String(72), nullable=False)
    name = db.Column(db.String(80))
    last_name = db.Column(db.String(120))
    city = db.Column(db.String(80))
    zip_code = db.Column(db.Integer)
    street = db.Column(db.String(150))
    house_number = db.Column(db.Integer)
    flat_number = db.Column(db.Integer)
    admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.token_id


class Grave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    day_of_birth = db.Column(db.DateTime(), nullable=False)
    day_of_death = db.Column(db.DateTime(), nullable=True)


class Parcel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parcel_type_id = db.Column(db.Integer, db.ForeignKey('parcel_type.id'), nullable=False)
    position_x = db.Column(db.Integer, nullable=False)
    position_y = db.Column(db.Integer, nullable=False)


class ParcelType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120))


class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grave_id = db.Column(db.Integer, db.ForeignKey('grave.id'), nullable=False)


class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.id'), nullable=False)
    date_of_payments = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime(), nullable=False)

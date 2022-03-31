from marshmallow import Schema, fields, validate
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import bcrypt
import datetime


user_info_db = SQLAlchemy()


class user_info_table(user_info_db.Model):
    __tablename__ = 'user_info'

    ID = user_info_db.Column(user_info_db.Integer,
                             primary_key=True, autoincrement=True)
    Email = user_info_db.Column(
        user_info_db.String(1000, 'utf8mb4_unicode_ci'))
    age = user_info_db.Column(user_info_db.Integer)
    sex = user_info_db.Column(user_info_db.String(1000, 'utf8mb4_unicode_ci'))
    weight = user_info_db.Column(
        user_info_db.Integer)
    height = user_info_db.Column(
        user_info_db.Integer)
    exercise = user_info_db.Column(
        user_info_db.String(1000, 'utf8mb4_unicode_ci'))
    disease = user_info_db.Column(
        user_info_db.String(1000, 'utf8mb4_unicode_ci'))
    drink = user_info_db.Column(
        user_info_db.String(1000, 'utf8mb4_unicode_ci'))
    smoke = user_info_db.Column(
        user_info_db.String(1000, 'utf8mb4_unicode_ci'))
    datetime = user_info_db.Column(
        user_info_db.DateTime, default=datetime.datetime.now)

    def __init__(self, Email, age, sex, weight, height, exercise, disease, drink, smoke):
        self.Email = Email
        self.age = age
        self.sex = sex
        self.weight = weight
        self.height = height
        self.exercise = exercise
        self.disease = disease
        self.drink = drink
        self.smoke = smoke

    # 정보 추가
    def add_user(Email, age, sex, weight, height, exercise, disease, drink, smoke):
        user = user_info_table(Email, age, sex, weight, height,
                               exercise, disease, drink, smoke)
        user_info_db.session.add(user)
        user_info_db.session.commit()
        return jsonify({'massage': 'Success', 'status': True})

    # 정보 조회
    def search(Email):
        user = user_info_table.query.filter(
            (user_info_table.Email == Email)).all()

        weight = []
        time = []

        for i in user:
            weight.append(i.weight)
            time.append(i.datetime)

        return weight, time

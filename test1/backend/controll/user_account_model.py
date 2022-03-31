from marshmallow import Schema, fields, validate
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import bcrypt


user_account_db = SQLAlchemy()


class UserTable(user_account_db.Model):
    __tablename__ = 'user_account'

    ID = user_account_db.Column(
        user_account_db.Integer, primary_key=True, autoincrement=True)
    Email = user_account_db.Column(
        user_account_db.String(1000, 'utf8mb4_unicode_ci'))
    name = user_account_db.Column(
        user_account_db.String(1000, 'utf8mb4_unicode_ci'))
    pw = user_account_db.Column(
        user_account_db.String(1000, 'utf8mb4_unicode_ci'))

    def __init__(self, Email, name, pw):
        self.Email = Email
        self.name = name
        self.pw = pw

    # 유저 추가
    def add_user(email, name, pw):
        hash_pw = bcrypt.hashpw(
            pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = UserTable.find_user(email, pw)
        if (user.json['status'] == False) & (user.json['massage'] == 'email'):
            user = UserTable(email, name, hash_pw)
            user_account_db.session.add(user)
            user_account_db.session.commit()
            return jsonify({'massage': 'Success', 'status': True})
        else:
            return jsonify({'massage': 'ID', 'status': False})

    # 유저 조회
    def find_user(email, pw):
        user = UserTable.query.filter((UserTable.Email == email)).first()

        if user is None:
            return jsonify({'massage': 'email', 'status': False})
        else:
            db_pw = user.pw
            result = bcrypt.checkpw(pw.encode(
                'utf-8'), db_pw.encode('utf-8'))
            if result == True:
                return jsonify({'massage': 'Success', 'status': True})
            else:
                return jsonify({'massage': 'PW', 'status': False})


# class UsersSchema(MA.Schema):
#     not_blank = validate.Length(min=1, error='Field cannot be blank')
#     id = fields.Integer(dump_only=True)
#     user_id = fields.String(validate=not_blank)
#     user_pw = fields.String(validate=not_blank)

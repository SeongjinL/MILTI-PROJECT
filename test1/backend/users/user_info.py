from matplotlib.font_manager import json_dump
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import request, jsonify, make_response
from flask_restx import Resource, Api, Namespace, fields
import json
from flask import redirect, url_for
from controll.user_info_model import user_info_table
import datetime
import jwt


user_info = Namespace('user_info')

user_email_fields = user_info.model('email', {  # Model 객체 생성
    'user_email': fields.String(description='email', required=True)
})

user_age_fields = user_info.inherit('User_email', user_email_fields, {
    'user_age': fields.String(description='age')
})

user_sex_fields = user_info.inherit('User_age', user_age_fields, {
    'user_sex': fields.String(description='sex')
})

user_weight_fields = user_info.inherit('User_sex', user_sex_fields, {
    'user_weight': fields.String(description='weight')
})

user_height_fields = user_info.inherit('User_weight', user_weight_fields, {
    'user_height': fields.String(description='height')
})

user_exercise_fields = user_info.inherit('User_height', user_height_fields, {
    'user_exercise': fields.String(description='exercise')
})

user_disease_fields = user_info.inherit('User_exercise', user_exercise_fields, {
    'user_disease': fields.String(description='disease')
})

user_drink_fields = user_info.inherit('User_disease', user_disease_fields, {
    'user_drink': fields.String(description='drink')
})

user_smoke_fields = user_info.inherit('User_drink', user_drink_fields, {
    'user_smoke': fields.String(description='smoke')
})


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other classes
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


@user_info.route('/')
class UserAccount(Resource):
    @user_info.expect(user_smoke_fields)
    @user_info.response(200, 'Success', user_smoke_fields)
    def post(self):
        '''기타 정보 추가'''
        data = request.get_json()
        user_email = list(filter(lambda x: 'user_email' in x,
                                 data['user_email'].split(';')))[0].split('=')[1]
        user_age = data['user_age']
        user_sex = data['user_sex']
        user_weight = data['user_weight']
        user_height = data['user_height']
        user_exercise = data['user_exercise']
        user_disease = data['user_disease']
        user_drink = data['user_drink']
        user_smoke = data['user_smoke']

        result = user_info_table.add_user(user_email, user_age, user_sex, user_weight, user_height,
                                          user_exercise, user_disease, user_drink, user_smoke)

        # return result
        return 'heell'

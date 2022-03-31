from matplotlib.font_manager import json_dump
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import request, jsonify, make_response
from flask_restx import Resource, Api, Namespace, fields
import json
from flask import redirect, url_for
from controll.user_account_model import UserTable
from controll.user_info_model import user_info_table
import datetime
import jwt


user_account = Namespace('user_account')

user_email_fields = user_account.model('email', {  # Model 객체 생성
    'user_email': fields.String(description='email', required=True)
})

user_pw_fields = user_account.inherit('User_email', user_email_fields, {
    'user_pw': fields.String(description='pw')
})

user_name_fields = user_account.inherit('User_pw', user_pw_fields, {
    'user_name': fields.String(description='name')
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


@user_account.route('/')
class UserAccount(Resource):
    @user_account.expect(user_pw_fields)
    @user_account.response(200, 'Success', user_pw_fields)
    def post(self):
        '''userid 체크 (로그인) true false tag id = user_id, user_pw'''
        user_email = request.json['user_email']
        user_pw = request.json['user_pw']

        result = UserTable.find_user(user_email, user_pw)

        if result.json['status'] == True:
            token = jwt.encode({'user_id': user_email, 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},
                               'secret', algorithm='HS256')
            weight, time = user_info_table.search(user_email)

            return jsonify({'massage': 'Success', 'status': True, 'token': token, 'user_email': user_email, 'weight': weight, 'time': time})
        else:
            return result

    @user_account.expect(user_name_fields)
    @user_account.response(200, 'Success', user_name_fields)
    def put(self):
        '''userid 회원가입 true false tag id = user_id2, user_pw2'''
        user_email = request.json['user_email']
        user_name = request.json['user_name']
        user_pw = request.json['user_pw']
        user_pw2 = request.json['user_pw2']
        if user_pw != user_pw2:
            return ({'massage': 'pw difference', 'status': False})

        else:
            result = UserTable.add_user(user_email, user_name, user_pw)

            if result.json['status'] is True:
                return jsonify({'massage': 'Success', 'status': True})
            else:
                return result

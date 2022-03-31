from flask import Flask, jsonify, request, session, render_template, make_response,  flash, redirect, url_for, send_file, make_response, Response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
import flask
import matplotlib
from control.user_mgmt import User
import os
from flask_pymongo import PyMongo
from datetime import timedelta, datetime
from werkzeug.utils import secure_filename
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from functools import wraps, update_wrapper
from flask_caching import Cache

import jwt
import datetime

matplotlib.use('Agg')


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'any random string'

app.config['MONGO_URI'] = 'mongodb://multi:multi@localhost:27017/user?authSource=admin'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DBNAME'] = 'user'
app.config['MONGO_USERNAME'] = 'multi'
app.config['MONGO_PASSWORD'] = 'multi'
app.config['MONGO_AUTH_SOURCE'] = 'admin'
app.config["PERMANET_SESSION_LIFETIME"] = timedelta(minutes=30)
# cache = Cache(config={'CACHE_TYPE': 'simple'})
# cache.init_app(app)

mongo = PyMongo(app)
# CORS(app)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@login_manager.user_loader
def load_user(token):
    return User.get(token)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.route('/check', methods=['POST'])
def check():
    user_id = request.form.get('id')
    user_pw = request.form.get('pw')
    data = User.get(user_id)
    print(data)
    # return render_template('login.html')
    if data is None:
        flash('회원정보가 없습니다')
        return redirect(url_for('login'))
    else:
        if data.user_pw == user_pw:
            # session['id'] = str(data.id)
            # session.permanent = True
            login_user(data)
            flash('로그인 되었습니다')
            return redirect(url_for('home'))
        else:
            flash('비밀번호가 일치하지 않습니다')
            return redirect(url_for('login'))


@app.route('/create', methods=['POST'])
def log1():
    return render_template('create.html')


# @app.route('/jwt')
# def check_jwt():
#     token = request.headers.get('token')
#     user_id = request.headers.get('user_id')
#     payload = {
#         'user_id': user_id,
#         'exp': datetime.datetime.utcnow()
#     }
#     test = jwt.encode(payload, 'secret', algorithm='HS256')
#     test1 = jwt.decode(test, 'secret', algorithms='HS256')
#     test2 = jwt.decode(token, 'secret', algorithms='HS256')
#     print(test1['exp'])
#     print(test2['exp'])
#     print(test1['exp'] < test2['exp'])
#     print(test2['exp'] - test1['exp'])
#     print(test2)
#     session['token'] = token
#     session['user_id'] = test2['user_id']


# def hoho(token, user_id):
#     token = session['token']
#     user_id = session['user_id']
#     payload = {
#         'user_id': user_id,
#         'exp': datetime.datetime.utcnow()}
#     try:
#         test = jwt.encode(payload, 'secret', algorithm='HS256')
#         test1 = jwt.decode(test, 'secret', algorithms='HS256')
#         test2 = jwt.decode(token, 'secret', algorithms='HS256')
#     except jwt.ExpiredSignatureError:
#         del session['token']
#         del session['user_id']
#     print('session', session)

    # print('test', test)
    # print('test1', test1)
    # print('test2', test2)

    # print(test1 < test2)

@app.route('/test')
def test123():
    # token = request.cookies.get('token')
    # user_email = request.cookies.get('user_email')
    # weight = request.cookies.get('weight')
    time = request.cookies.get('time')

    print(time)

    # try:
    #     jwt.decode(token, 'secret', algorithms='HS256')
    #     session['token'] = token
    #     session['time'] = time
    #     return redirect(url_for('home'))
    # except jwt.ExpiredSignatureError:
    #     flash('일정 시간이 지나 다시 로그인 해야합니다')
    #     return redirect(url_for("login"))
    # except jwt.exceptions.DecodeError:
    #     flash('다시 로그인 하세요')
    #     print(session)
    #     return redirect(url_for("login"))


@app.route('/')
def home():
    print(session)
    if 'token' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/login')
def login():
    if 'token' in session:
        flash('이미 로그인된 상태입니다')
        return redirect(url_for('home'))
    else:
        return render_template('login.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/logout')
def logout():
    if 'token' in session:
        session.pop('token')
        return redirect(url_for('login'))
    else:
        flash('로그인을 해야 합니다')
        return redirect(url_for('login'))


@app.route('/check2', methods=['POST'])
def check2():
    user_id = request.form.get('id')
    user_pw = request.form.get('pw')
    user_pw2 = request.form.get('pw2')

    if user_id == '' or user_pw == '' or user_pw2 == '':
        flash('입력되지 않은 값이 있습니다')
        return render_template('create.html')

    if user_pw != user_pw2:
        flash('비밀번호가 일치하지 않습니다')
        return render_template('create.html')

    data = User.get(user_id)

    if data is not None:
        flash('사용할 수 없는 ID입니다')
        return render_template('create.html')

    User.create(user_id, user_pw)
    flash('회원가입이 완료되었습니다')
    return render_template('login.html')


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


# @app.route('/uploader', methods=['GET', 'POST'])
# def uploader_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save('/home/lab05/babbu_mysql_ver_0325/static/' +
#                secure_filename(f.filename))
#         print('session', session)
#         if current_user.is_authenticated:
#             Image.create(
#                 current_user.id, secure_filename(f.filename))

#             return 'file uploaded successfully'


# @app.route('/list', endpoint='list')
# @login_required
# def blog():
#     data = Image.get(current_user.id)
#     result = []
#     if data is not None:
#         for i in data:
#             result.append(i[2])
#         return render_template('list.html', value=result)
#     else:
#         return render_template('index.html')
    # if session['id'] is not None:
    #     data = Image.get(session['id'])
    #     result = []
    #     if data is not None:
    #         for i in data:
    #             result.append(i[2])

    #         return render_template('list.html', value=result)
    #     else:
    #         return render_template('index.html')


@app.route('/normal')
@login_required
def normal():
    if current_user.is_authenticated:
        return render_template("graph.html", width=800, height=600)


# @app.route('/fig')
# def fig():

#     plt.figure(figsize=(6, 7))

#     data = list(Info.find(current_user.id))

#     weight = []
#     date = []
#     for i in range(len(data)):
#         weight.append(data[i][0])
#         date.append(data[i][1])

#     plt.plot(date, weight)
#     img = BytesIO()
#     plt.savefig(img, format='png', dpi=300)
#     img.seek(0)
#     return send_file(img, mimetype='image/png')


'''
몸무게, 시간등 부가적인 정보 넣는 부분
'''
# @app.route('/info', methods=['GET', 'POST'])
# def info():
#     if request.method == 'POST':
#          weight = request.form.get('weight')
#         if 'id' in session:
#             info.create(
#                 session['id'], weight)

#             return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8989', debug=True)

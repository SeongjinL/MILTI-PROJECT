from flask import Flask, jsonify, request, session, render_template, make_response,  flash, redirect, url_for, send_file, make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
import flask
import matplotlib
from control.user_mgmt import User
from control.user_mgmt import Image
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
from control.user_mgmt import Info

matplotlib.use('Agg')


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')

app.config['MONGO_URI'] = 'mongodb://multi:multi@localhost:27017/user?authSource=admin'
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DBNAME'] = 'user'
app.config['MONGO_USERNAME'] = 'multi'
app.config['MONGO_PASSWORD'] = 'multi'
app.config['MONGO_AUTH_SOURCE'] = 'admin'
app.config["PERMANET_SESSION_LIFETIME"] = timedelta(minutes=600)
# cache = Cache(config={'CACHE_TYPE': 'simple'})
# cache.init_app(app)

mongo = PyMongo(app)
CORS(app)
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
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)


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
            session['id'] = str(data.id)
            session.permanent = True
            flash('로그인 되었습니다')
            return redirect(url_for('home'))
        else:
            flash('비밀번호가 일치하지 않습니다')
            return redirect(url_for('login'))


@app.route('/create', methods=['POST'])
def log1():
    return render_template('create.html')


@app.route('/')
def home():
    print(session)

    return render_template('index.html')


@app.route('/login')
def login():
    if session.get('id', None) is not None:

        return redirect(url_for('home'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    if session.get('id', None) is not None:
        session.pop('id')
        return redirect(url_for('home'))
    else:
        flash('로그인을 해야 합니다')
        return redirect(url_for('home'))


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


@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('/home/lab05/babbu/static/' + secure_filename(f.filename))
        print('session', session)
        if session['id'] is not None:
            Image.create(
                session['id'], secure_filename(f.filename))

            return 'file uploaded successfully'


@app.route('/list', endpoint='list')
def blog():
    if session['id'] is not None:
        data = Image.get(session['id'])
        result = []
        if data is not None:
            for i in data:
                result.append(i[2])

            return render_template('list.html', value=result)
        else:
            return render_template('index.html')


@app.route('/normal')
def normal():
    if 'id' in session:
        return render_template("graph.html", width=800, height=600)


@app.route('/fig')
def fig():

    plt.figure(figsize=(6, 7))

    data = list(Info.find(session['id']))

    weight = []
    date = []
    for i in range(len(data)):
        weight.append(data[i][0])
        date.append(data[i][1])

    plt.plot(date, weight)
    img = BytesIO()
    plt.savefig(img, format='png', dpi=300)
    img.seek(0)
    return send_file(img, mimetype='image/png')


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

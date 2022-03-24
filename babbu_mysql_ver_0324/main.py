from flask import Flask, jsonify, request, session, render_template, make_response,  flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from control.user_mgmt import User
import os
from flask_pymongo import PyMongo
from datetime import timedelta
from werkzeug.utils import secure_filename
from bson import json_util
import pymysql


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
mongo = PyMongo(app)
CORS(app)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'


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
    members = mongo.db.members
    data = members.find_one({'user_id': user_id})
    print('data', data)
    if data is None:
        flash('회원정보가 없습니다')
        return redirect(url_for('login'))
    else:
        if data.get('user_pw') == user_pw:
            session['id'] = str(data.get('_id'))
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
    print(mongo.db.member)

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

    members = mongo.db.members
    data = members.find({'user_id': user_id})
    result = []
    for i in data:
        result.append(i)

    if len(result) > 0:
        flash('사용할 수 없는 ID입니다')
        return render_template('create.html')
    post = {
        'user_id': user_id,
        'user_pw': user_pw,
    }
    members.insert_one(post)
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
            images = mongo.db.images
            post = {
                'user_id': session['id'],
                'image': secure_filename(f.filename),
            }
            images.insert_one(post)

            return 'file uploaded successfully'


@app.route('/list')
def blog():
    if session['id'] is not None:
        images = mongo.db.images
        result = images.find({'user_id': session['id']})
        result = list(result)
        for i in result:
            print(i)

        return render_template('list.html', value=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8989', debug=True)

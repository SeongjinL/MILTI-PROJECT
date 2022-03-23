from flask import Flask, Blueprint, session, render_template, make_response, jsonify, redirect, url_for
from flask import request, flash
from flask_login import login_user, current_user, logout_user


bappu = Blueprint('bappu', __name__)


@bappu.route('/check', methods=['POST'])
def check():
    user_id = request.form.get('id')
    user_pw = request.form.get('pw')

    members = MONGO_CONN.db.members
    data = members.find_one({'user_id': user_id})

    if data is None:
        flash('회원정보가 없습니다')
        return redirect(url_for('login'))
    else:
        if data.get('pwd') == user_pw:
            session['id'] = str(data.get('_id'))
            session.permanent = True
            return redirect(url_for('/'))
        else:
            flash('비밀번호가 일치하지 않습니다')
            return redirect(url_for('login'))


@bappu.route('/create', methods=['POST'])
def log1():
    return render_template('create.html')


@bappu.route('/')
def home():
    return render_template('index.html')


@bappu.route('/login')
def login():
    return render_template('login.html')


@bappu.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for('index.html'))


@bappu.route('/check2')
def check2():
    if current_user.is_authenticated:
        webpage_name = BlogSession.get_blog_page(current_user.blog_id)
        BlogSession.save_session_info(
            session['client_id'], current_user.user_email, webpage_name)
        return render_template(webpage_name, user_email=current_user.user_email)
    else:
        webpage_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(
            session['client_id'], 'anonymous', webpage_name)
        return render_template(webpage_name)

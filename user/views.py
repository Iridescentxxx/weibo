from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import session

from libs.orm import db
from user.models import User

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_bp.template_folder = './templates'


@user_bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phonenum = request.form.get('phonenum')
        gender = request.form.get('gender')

        user = User(username=username, password=password, phonenum=phonenum, gender=gender)
        db.session.add(user)
        db.session.commit()
        return redirect('/user/login')
    else:
        return render_template('register.html')


@user_bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user = User.query.filter_by(username=username).one()
        except Exception:
            db.session.rollback()
            return '用户昵称错误'

        if password and user.password == password:
            session['uid'] = user.id
            session['username'] = user.username
            return redirect('/user/info')
        else:
            return '密码错误'
    else:
        return render_template('login.html')


@user_bp.route('/info')
def info():
    uid = session['uid']
    user = User.query.get(uid)
    return render_template('info.html', user=user)


@user_bp.route('/logout')
def logout():
    return redirect('/user/login')

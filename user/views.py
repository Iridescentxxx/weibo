import datetime

from flask import Blueprint
from flask import request
from flask import redirect
from flask import session
from flask import render_template
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from libs.orm import db
from libs.utils import make_password
from libs.utils import check_password
from libs.utils import save_avatar
from libs.utils import login_required
from user.models import User

user_bp = Blueprint('user', __name__, url_prefix='/user', template_folder='./templates')


@user_bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password1 = request.form.get('password1', '').strip()
        password2 = request.form.get('password2', '').strip()
        gender = request.form.get('gender', '').strip()
        birthday = request.form.get('birthday', '').strip()
        city = request.form.get('city', '').strip()
        bio = request.form.get('bio', '').strip()
        now = datetime.datetime.now()  # 注册时间

        if not password1 or password1 != password2:
            return render_template('register.html', err='密码不符合要求')

        user = User(nickname=nickname, password=make_password(password1),
                    gender=gender, birthday=birthday, city=city, bio=bio, created=now)

        # 保存头像
        avatar_file = request.files.get('avatar')
        if avatar_file:
            user.avatar = save_avatar(avatar_file)

        try:
            # 保存到数据库
            db.session.add(user)
            db.session.commit()
            return redirect('/user/login')
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', err='您的昵称已被占用')
    else:
        return render_template('register.html')


@user_bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()

        # 获取用户
        try:
            user = User.query.filter_by(nickname=nickname).one()
        except NoResultFound:
            return render_template('login.html', err='该用户不存在')

        # 检查密码
        if check_password(password, user.password):
            # 在 Session 中记录用户的登录状态
            session['uid'] = user.id
            session['nickname'] = user.nickname
            return redirect('/user/info')
        else:
            return render_template('login.html', err='密码错误')
    else:
        return render_template('login.html')


@user_bp.route('/logout')
def logout():
    '''退出功能'''
    session.clear()
    return redirect('/')


@user_bp.route('/info')
@login_required
def info():
    '''查看用户信息'''
    uid = session['uid']
    user = User.query.get(uid)
    return render_template('info.html', user=user)

import os
import random
from functools import wraps
from hashlib import md5, sha256

from flask import session
from flask import redirect


def make_password(password):
    '''产生一个安全密码'''
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')

    hash_value = sha256(password).hexdigest()
    salt = os.urandom(16).hex()
    safe_password = salt + hash_value

    return safe_password


def check_password(password, safe_password):
    '''检查密码'''
    if not isinstance(password, bytes):
        password = str(password).encode('utf8')

    # 计算哈希值
    hash_value = sha256(password).hexdigest()

    return hash_value == safe_password[32:]


def save_avatar(avatar_file):
    '''保存头像文件'''
    file_bin_data = avatar_file.stream.read()
    avatar_file.stream.seek(0)
    filename = md5(file_bin_data).hexdigest()

    # 获取项目文件夹的绝对路径
    base_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    # 文件绝对路径
    filepath = os.path.join(base_dir, 'static', 'upload', filename)
    # 保存文件
    avatar_file.save(filepath)
    # 文件的 URL
    avatar_url = f'/static/upload/{filename}'

    return avatar_url


def login_required(view_func):
    @wraps(view_func)
    def check_session(*args, **kwargs):
        uid = session.get('uid')
        if not uid:
            return redirect('/user/login')
        else:
            return view_func(*args, **kwargs)

    return check_session


def random_zh_str(length):
    '''随机产生出一个中文字符串'''
    words = [chr(random.randint(20000, 30000)) for i in range(length)]
    return ''.join(words)

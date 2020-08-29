import random

from libs.orm import db
from libs.utils import random_zh_str


class User(db.Model):
    '''用户表'''
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'unknow'), default='unknow')
    birthday = db.Column(db.Date, default='2000-01-01')
    city = db.Column(db.String(10), default='中国')
    avatar = db.Column(db.String(256), default='/static/img/default.png')
    bio = db.Column(db.Text, default='')
    created = db.Column(db.DateTime, nullable=False)  # 用户注册时间

    n_follow = db.Column(db.Integer, nullable=False, default=0)
    n_fans = db.Column(db.Integer, nullable=False, default=0)

    @classmethod
    def fake_users(cls, num):
        users = []
        for i in range(num):
            year = random.randint(1980, 2000)
            month = random.randint(1, 12)
            day = random.randint(1, 28)

            nickname = random_zh_str(3)
            password = '1234567890'
            gender = random.choice(['male', 'female', 'unknow'])
            birthday = '%04d-%02d-%02d' % (year, month, day)
            city = random.choice(['上海', '北京', '南京', '北海', '乌鲁木齐', '威海', '许昌', '郑州'])
            bio = random_zh_str(30)
            created = '2013-11-12'
            user = cls(nickname=nickname, password=password, gender=gender,
                       birthday=birthday, city=city, bio=bio, created=created)
            users.append(user)
        db.session.add_all(users)
        db.session.commit()
        return users

class Follow(db.Model):
    '''关注表'''
    __tablename__ = 'follow'

    uid = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, primary_key=True)
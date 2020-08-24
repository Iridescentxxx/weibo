from libs.orm import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128), nullable=False)
    phonenum = db.Column(db.Integer)
    gender = db.Column(db.String(20))
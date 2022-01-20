from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Float(10))
    mini_date = db.Column(db.String(10))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    avg_time = db.Column(db.Integer)
    min = db.Column(db.Integer)
    max = db.Column(db.Integer)
    entries = db.relationship('Entry')
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class Group(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(150), unique=True)
    users = db.relationship('User', backref="group", lazy='select')

import jwt
from flask_login import UserMixin
from app import db, login
from flask import current_app
from datetime import datetime


@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_reset_password_token(self):
        return jwt.encode({'id': self.id}, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def check_reset_password_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithm=['HS256'])
            return User.query.filter_by(id=data['id']).first()
        except:
            return

class Ski(db.Model):
    __bind_key__ = 'ski'
    id = db.Column(db.Integer, primary_key=True)
    ski_brand = db.Column(db.String(20), nullable=False)
    ski_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.String(20), nullable=False)
    detail_date = datetime.now()
    create_date = db.Column(db.DateTime, nullable=False, default=detail_date)
    modification_time = db.Column(db.DateTime, nullable=False, default=detail_date)

    def __init__(self, ski_brand, ski_type, price, availability):
        self.ski_brand = ski_brand
        self.ski_type = ski_type
        self.price = price
        self.availability = availability

    def __repr__(self):
        return '<Ski %r>' % self.ski_brand
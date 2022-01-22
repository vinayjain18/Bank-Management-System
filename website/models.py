from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150))
	email = db.Column(db.String(150))
	mobile = db.Column(db.Integer)
	aadhar = db.Column(db.Integer)
	account = db.Column(db.Integer, unique=True)
	password = db.Column(db.String(150))
	transacts = db.relationship('Transact')


class Transact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	withdraw = db.Column(db.Float, default=0)
	deposit = db.Column(db.Float, default=0)
	balance = db.Column(db.Float)
	date = db.Column(db.DateTime(timezone=True), default=func.now())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
import os


db = SQLAlchemy()
mail = Mail()
DB_NAME = "database.db"

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USERNAME'] = os.environ['USER']
	app.config['MAIL_PASSWORD'] = os.environ['PASSWORD']
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL'] = True
	mail.init_app(app)
	db.init_app(app)

	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	from .models import User, Transact

	create_database(app)

	admin = Admin(app)
	admin.add_view(ModelView(User, db.session))
	admin.add_view(ModelView(Transact, db.session))

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))


	return app


def create_database(app):
	if not path.exists('website/'+DB_NAME):
		db.create_all(app=app)
		print("Created successfully")

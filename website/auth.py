from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Transact
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_required, logout_user, login_user
from . import db, mail
from flask_mail import Message
import random

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		account = request.form.get('account')
		password = request.form.get('password')

		user = User.query.filter_by(account=account).first()

		if account =="":
			flash('Enter Bank Account number', category='error')

		elif password == "":
			flash('Enter password', category='error')

		elif user:
			if check_password_hash(user.password, password):
				flash('Logged-in successfully', category='success')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('Incorrect password, try again', category='error')

		else:
			flash('This Account number doesn\'t exists. Please Sign-Up', category='error')
			return redirect(url_for('auth.sign_up'))


	return render_template('login.html', user = current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

	#Below I have created a function to generate random account number for user.
	def create_account_number():
		acc = ""
		for i in range(10):
			n = random.randint(0, 9)
			acc += str(n)
		return acc

	acc = int(create_account_number())  


	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		mobile = request.form.get('mobile')
		aadhar = request.form.get('aadhar')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		user = User.query.filter_by(mobile=mobile).first()

		if user:
			flash(f'This User already have bank account with this mobile number. Please Login', category='error')
			return redirect(url_for('auth.login'))
		elif len(name) < 2:
			flash('Enter name correctly', category='error')
		elif len(email) < 4:
			flash('Email is too short', category='error')
		elif len(mobile) != 10:
			flash('Mobile number is incorrect', category='error')
		elif len(aadhar) != 12:
			flash('Aadhar number is incorrect', category='error')
		elif password1 != password2:
			flash('Password is not matching, Try again!', category='error')
		elif len(password1) < 7:
			flash('Password must be greater than 7 characters.', category='error')
		else:
			new_user = User(name=name, email=email, mobile=mobile, aadhar=aadhar,account=acc, password=generate_password_hash(password1, method='sha256'))
			db.session.add(new_user)
			db.session.commit()
			new_account = Transact(balance=0, user_id = new_user.id)
			db.session.add(new_account)
			db.session.commit()
			msg = Message('Welcome to Apna Bank', sender = ('Apna Bank','bankapna20@gmail.com'), recipients = [email])
			msg.body = f"Your account has been successfully created with Apna Bank.\n\nBelow is your login details:\nAccount number: {acc}\nPassword: You entered while sign-up."
			mail.send(msg)
			flash('Your login details has been sent to registered email.', category='success')
			return redirect(url_for('auth.login'))

	return render_template('sign_up.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('views.home'))
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from .models import User, Transact
from . import db
import sqlalchemy


views = Blueprint('views', __name__)


@views.route('/')
def home():
	data = User.query.all()
	trans = Transact.query.all()
	return render_template('home.html', user = current_user, db = data, trans = trans)


@views.route('/service', methods = ['POST', 'GET'])
@login_required
def service():
	trans = Transact.query.filter_by(user_id = current_user.id).order_by(sqlalchemy.desc(Transact.id)).first()
	if request.method == 'POST':
		data = request.form
		print(data)
		if 'withdraw' in data:
			try:
				withdraw = float(request.form.get('withdraw'))
				if withdraw > trans.balance:
					flash(f"Your Account has only ₹{trans.balance}", category='error')
				else:
					balance = trans.balance - withdraw
					transaction = Transact(withdraw = withdraw, balance = balance, user_id = current_user.id)
					db.session.add(transaction)
					db.session.commit()
					flash('Amount withdrawn successfully.', category='success')
					return redirect(url_for('views.service', user = current_user))
			except:
				flash("Enter number only.", category='error')
				return redirect(request.url)


		if 'deposit' in data:
			try:
				deposit = float(request.form.get('deposit'))
				balance = trans.balance + deposit
				transaction = Transact(deposit = deposit, balance = balance, user_id = current_user.id)
				db.session.add(transaction)
				db.session.commit()
				flash('Amount deposited successfully.', category='success')
				return redirect(url_for('views.service', user = current_user))
			except:
				flash("Enter number only.", category='error')
				return redirect(request.url)


	return render_template('service.html', user = current_user, trans = trans)


@views.route('/transaction')
@login_required
def transaction():
	return render_template('transact.html', user = current_user)
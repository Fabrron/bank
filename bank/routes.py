import os
from datetime import datetime
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from bank import app, db, bcrypt, mail
from bank.forms import RegistrationForm, LoginForm, UpdateAccountForm
from bank.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(
			form.password.data).decode('utf-8')
		user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, \
			phone=form.phone.data, street=form.street.data, city=form.city.data, state=form.state.data, \
			country=form.country.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect('login')


@app.route('/')
@app.route('/home')
@login_required
def home():
	return render_template('index.html')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.firstname = form.firstname.data
		current_user.lastname = form.lastname.data
		current_user.email = form.email.data
		current_user.phone = form.phone.data
		current_user.street = form.street.data
		current_user.city = form.city.data
		current_user.state = form.state.data
		current_user.country = form.country.data
		current_user.debit = form.debit.data
		current_user.credit = form.credit.data
		current_user.currency = form.currency.data
		db.session.commit()
		flash('Your Account has been updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.firstname.data = current_user.firstname
		form.lastname.data = current_user.lastname
		form.email.data = current_user.email
		form.phone.data = current_user.phone
		form.street.data = current_user.street
		form.city.data = current_user.city
		form.state.data = current_user.state
		form.country.data = current_user.country
		form.debit.data = current_user.debit
		form.credit.data = current_user.credit
		form.currency.data = current_user.currency
	return render_template('account.html', title='Account', form=form)

@app.route('/admin')
@login_required
def admin():
	users = User.query.all()
	if current_user.email != "deanpeterson@hallmarkfinancing.com":
		return redirect(url_for('home'))
	return render_template('admin.html', users=users)

@app.route('/admin/delete/<string:phone>')
@login_required
def admin_delete_account(phone):
	user = User.query.filter_by(phone=phone).first()
	if current_user.email == 'deanpeterson@hallmarkfinancing.com':
		db.session.delete(user)
		db.session.commit()
		flash('Account Successfully deleted by Admin.', 'success')
	return redirect(url_for('admin', user=user))


@app.route('/beneficiaries/manage-beneficiaries')
@login_required
def mb():
	return render_template('managebeneficiaries.html')

@app.route('/beneficiaries/add-beneficiaries')
@login_required
def ab():
	return render_template('addbeneficiary.html')

@app.route('/transfer/to-this-bank')
@login_required
def ttb():
	return render_template('tothisbank.html')

@app.route('/transfer/to-other-bank')
@login_required
def tob():
	return render_template('tootherbanks.html')

@app.route('/transfer/to-beneficiary')
@login_required
def tb():
	return render_template('tobeneficiaries.html')

@app.route('/transfer/international')
@login_required
def international():
	return render_template('international.html')

@app.route('/transactions/to-this-bank')
@login_required
def tr_ttb():
	return render_template('tr_tothisbank.html')

@app.route('/transactions/to-other-bank')
@login_required
def tr_tob():
	return render_template('tr_otherbanks.html')

@app.route('/transactions/to-beneficiary')
@login_required
def tr_tb():
	return render_template('tr_tobeneficiary.html')

@app.route('/transactions/international')
@login_required
def tr_international():
	return render_template('tr_international.html')

@app.route('/support')
@login_required
def support():
	return render_template('support.html')

@app.route('/profile')
@login_required
def profile():
	return render_template('profile.html')

























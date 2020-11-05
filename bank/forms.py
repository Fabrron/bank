from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, DateField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from bank.models import User

class RegistrationForm(FlaskForm):
	firstname = StringField('First Name', validators=[DataRequired()])
	lastname = StringField('Last Name', validators=[DataRequired()])
	email = StringField('Email', validators = [Email(), DataRequired()])
	phone = StringField('Phone', validators=[DataRequired()])
	street = StringField('Street', validators=[DataRequired()])
	city = StringField('City', validators=[DataRequired()])
	state = StringField('State', validators=[DataRequired()])
	country = StringField('Country', validators=[DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one')

	def validate_phone(self, phone):
		user = User.query.filter_by(phone=phone.data).first()
		if user:
			raise ValidationError('That phone number is taken. Please choose a different one')


class LoginForm(FlaskForm):
	email = StringField('Email', validators = [Email(), DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	firstname = StringField('First Name', validators=[DataRequired()])
	lastname = StringField('Last Name', validators=[DataRequired()])
	email = StringField('Email', validators = [DataRequired(), Email()])
	phone = StringField('Phone', validators=[DataRequired()])
	street = StringField('Street', validators=[DataRequired()])
	city = StringField('City', validators=[DataRequired()])
	state = StringField('State', validators=[DataRequired()])
	country = StringField('Country', validators=[DataRequired()])
	debit = StringField('Debit', validators=[DataRequired()])
	credit = StringField('Credit', validators=[DataRequired()])
	submit = SubmitField('Update')












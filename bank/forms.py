from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, DateField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from bank.models import User

class RegistrationForm(FlaskForm):
	email = StringField('Email', validators = [Email(), DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one')


class LoginForm(FlaskForm):
	email = StringField('Email', validators = [Email(), DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

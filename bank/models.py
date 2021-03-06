from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bank import db, login_manager, app
from flask_login import UserMixin
from markdown import markdown
import bleach



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(120), nullable=True)
	lastname = db.Column(db.String(120), nullable=True)
	email = db.Column(db.String(120), unique=True, nullable=True)
	phone = db.Column(db.String(120), unique=True, nullable=True)
	street = db.Column(db.String(120), nullable=True)
	city = db.Column(db.String(120), nullable=True)
	state = db.Column(db.String(120), nullable=True)
	country = db.Column(db.String(120), nullable=True)
	debit = db.Column(db.String(120), nullable=True, default="0.00")
	credit= db.Column(db.String(120), nullable=True, default="2,500,000.00")
	currency = db.Column(db.String(20), nullable=True, default="EURO")
	password = db.Column(db.String(60), nullable=False)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id' : self.id}).decode('utf-8')


	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)


	def __repr__(self):
		return f"User('{self.firstname}' , '{self.email}', '{self.phone}')"

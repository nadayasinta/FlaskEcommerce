from flask_restful import fields
from blueprint import db

class User(db.Model):
	__tablename__='user'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	username = db.Column(db.String(15), unique=True, nullable=False)
	password = db.Column(db.String(15), nullable=False)
	status = db.Column(db.Boolean, nullable=False)

	response_fields={
		'id':fields.Integer,
		'name':fields.String,
		'username':fields.String,
		'password':fields.String,
		'status':fields.Boolean,
	}

	transaction_response_fields={
		'id':fields.Integer,
		'name':fields.String,
		'username':fields.String,
	}

	def __init__(self, name, username, password, status):
		self.name=name
		self.username=username
		self.password=password
		self.status=status


	def __repr__(self):
		return '<User %r>' %self.id

	
	@classmethod
	def is_exists(cls, data):

		all_data = cls.query.all()

		existing_username = [item.username for item in all_data]

		if data in existing_username:
			return True

		return False
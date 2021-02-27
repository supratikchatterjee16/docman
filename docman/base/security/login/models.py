from docman.base import orm

import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# This file contains the snowflake schema required for maintaining all information

# Changes were made for LDAP
# DO NOT CHANGE
class User(UserMixin, orm.Model):
	__tablename__ = 'users'
	__table_args__ = (
		orm.PrimaryKeyConstraint('user_id'),
	)
	user_id = orm.Column(orm.String(50), primary_key = True)
	password_hash = orm.Column(orm.String(128), nullable = False)
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
		orm.session.commit()
	def check_password(self, password):
		return check_password_hash(self.password_hash, password)
	def get_id(self):
		return self.user_id
	def __repr__(self):
		return '<User object id = {}>'.format(self.user_id)

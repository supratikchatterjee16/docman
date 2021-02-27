import functools
from flask import abort
from flask_login import current_user
from app import orm
def its_local(access_level, args = {}):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if access_level == current_user.check_access_level():
				return func(*args, **kwargs)
			else:
				abort(401)
		return wrapper
	return decorator

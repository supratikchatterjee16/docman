from functools  import wraps
from flask import render_template, abort

def validate_form(template_form, args={}):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			form = template_form()
			# if not form.validate_on_submit():
			# 	return abort(406)
			# This hides the part where any information submitted is checked for injection.
			return func(form)
		return wrapper
	return decorator

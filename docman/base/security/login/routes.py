#Get the login_manager and the application to register routes
# Import flask specific components
from flask import redirect, render_template, url_for, abort, flash, make_response
from flask_login import login_required, login_user, logout_user, current_user

from docman.base.security.csrf import validate_form
from docman.base.security.local import its_local
from docman.base.security.admin import create_or_update_admin

from docman.base import login_manager, application

# Relatively import the forms for login
from . import forms, models

# This is the component that loads the user, do not make changes to this
# If the application fails to load a user, subsequent checks automatically fail
# causing an error page
@login_manager.user_loader
def user_loader(id):
	try:
		user = models.User.query.filter_by(user_id=id).first()
		if user:
			return user
		else:
			return None
	except Exception as e:
		return None

# Redirect logic for the 1st layer of security.
# No matter from where you enter, you shall be shown the door to enter.
@login_manager.unauthorized_handler
def unauthorized():
	print('Unauthorized execute')
	if not current_user.is_authenticated:
		# abort(401)
		return redirect('/login')

# GET methods only have sanity check and page delivery
@application.route('/login', methods=['GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = forms.LoginForm()
	response = make_response(render_template('login/login.jinja2', form=form))
	response.headers['Clear-Site-Data'] = '"cookies"'
	create_or_update_admin()
	return response

# Login process
# Only approved user can acquire the rights to gain access to the system
# If they haven't been approved, they will not be able to access anything
@application.route('/login', methods=['POST'])
@validate_form(forms.LoginForm)
def login_post(form): # Main login logic
	# Main logic
	user = models.User.query.filter_by(user_id=form.user_id.data).first()
	if user:
		if user.check_password(form.password.data):
			login_user(user)
			create_or_update_admin() # Change this as soon as we have a hit
			return redirect('/')
		# else:
		# 	try:
		# 		user.attempt_ldap(form.password.data)
		# 		user.set_password(form.password.data)
		# 		db.session.commit()
		# 	except:
		# 		return 'Credentials do not match'
	else:
		user = models.User(user_id = form.user_id.data)
		try:
			# user.attempt_ldap(form.password.data)
			user.set_password(form.password.data)
			user.status = 'N'
			db.session.add(user)
			db.session.commit()
		except:
			return 'Credentials do not match'
		return 'Credentials do not match'

# GET methods for signup
@application.route('/signup', methods=['GET'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = forms.SignupForm()
	return render_template('login/signup.jinja2', form=form)

# Signup process
# On signup a user is created and marked as new(N) in the User model
# This user needs to be approved(A) before they gain the ability to access anything
# The only addition that may be required is the creation of a captcha to prevent
# DDoS and pranks
@application.route('/signup', methods=['POST'])
@validate_form(forms.SignupForm)
def signup_post(form):
	user = models.User(
		user_id=form.user_id.data,
	)
	last_name = ''
	if form.last_name.data:
		last_name = form.last_name.data
	user.set_password(password = form.password.data)
	return redirect(url_for('index'))

# Process to log user out
@application.route('/logout')
@login_required
def logout():
	logout_user()
	response = make_response('ACK')
	response.headers['Clear-Site-Data'] = '"*"'
	return response, 200

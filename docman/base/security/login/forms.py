# Project ORDASH
# Module app.forms
# Author : Supratik Chatterjee
#
# This file is stable as of 23 May, 2019

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SelectMultipleField,IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
from .models import User

class LoginForm(FlaskForm):
	user_id =  StringField('ID', validators=[DataRequired()],render_kw={"placeholder": "Employee ID", 'autofocus' : True})
	password = PasswordField('Password', validators=[DataRequired(),Length(min=2,max=20)],render_kw={"placeholder": "Password"})
	#recaptcha = RecaptchaField()

class SignupForm(FlaskForm):
	user_id =  StringField('ID', validators=[DataRequired()],render_kw={"placeholder": "Employee ID", 'autofocus' : True})
	first_name = StringField('First Name', validators=[DataRequired(),Length(min=2,max=20)],render_kw={"placeholder": "First Name"})
	last_name = StringField('Last Name', render_kw={"placeholder": "Last Name"})
	password = PasswordField('Password', validators=[DataRequired() , Length(min=2,max=20), EqualTo('confirm_password')],render_kw={"placeholder": "Password"})
	confirm_password = PasswordField('Confirm', validators=[DataRequired()], render_kw={'placeholder' : 'Confirm Password'})
	#recaptcha = RecaptchaField()
	def validate_user_id(self, user_id):
		user = User.query.filter_by(user_id=user_id.data).first()
		if user:
			raise ValidationError('That User ID already exists')

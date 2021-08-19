# Forms for Registration and Login

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
  first_name = StringField("First Name", validators=[DataRequired()])
  last_name = StringField("Last Name", validators=[DataRequired()])
  email_address = StringField('Email Address', validators=[DataRequired(), Email()])
  username = StringField('Username', 
  validators=[DataRequired(), Length(min=5, max=20)])
  password = PasswordField('Password', 
  validators=[DataRequired(), Length(min=8, max=20)])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=20), EqualTo('password', message='Passwords must match')])
  submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
  username = StringField('Username', 
  validators=[DataRequired()])
  email_address = StringField('Email Address', validators=[DataRequired(), Email()])
  password = PasswordField('Password', 
  validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField("Login")
  
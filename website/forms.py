# Forms for Registration and Login

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website.models import User

# Registration Form Class
class RegistrationForm(FlaskForm):
  first_name = StringField("First Name", validators=[DataRequired()])
  last_name = StringField("Last Name", validators=[DataRequired()])
  email = StringField('Email Address', validators=[DataRequired(), Email()])
  username = StringField('Username', 
  validators=[DataRequired(), Length(min=5, max=20)])
  password = PasswordField('Password', 
  validators=[DataRequired(), Length(min=8, max=20)])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=20), EqualTo('password', message='Passwords must match')])
  submit = SubmitField("Create Account")
  
  # checks if the username exists in the database
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('Username is taken. Please choose a different username!')

  # checks if the email address exists in the database
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('Email address exists. Please use a different one!')

# Login Form Class
class LoginForm(FlaskForm):
  email = StringField('Email Address', validators=[DataRequired(), Email()])
  password = PasswordField('Password', 
  validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField("Login")
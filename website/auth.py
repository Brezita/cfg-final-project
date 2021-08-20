# authorisation

from website.forms import RegistrationForm, LoginForm
from flask import Blueprint, render_template, url_for, flash, redirect, request
from .views import views
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# defining this file is a Blueprint of our application, it has a group of URL's

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
  login_form = LoginForm()
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
        
    # checks to see if the user is in the database
    user = User.query.filter_by(email=email).first()

    # checks password entered matches the stored hashed password 
    if user:
      if check_password_hash(user.password, password):
        flash('Logged in successfully!', category='success')
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
      else:
        flash('Incorrect password, try again.', category='error')
  else:
      flash('Email does not exist.', category='error')

  return render_template("login.html", title='Login', form=login_form, boolean=True)

@auth.route('/register', methods=['GET', 'POST'])
def register():
  # creates an instance
  register_form = RegistrationForm()
  
  if register_form.validate_on_submit():
    if request.method == 'POST':
      # gets email address from form to run query
      email = request.form.get('email_address')

      # checks to see if the user is in the database
      user = User.query.filter_by(email=email).first()

      if user:
        flash('Email address already exists.', category='error')
      else:
        if register_form.validate_on_submit():
          flash(f'Account created for {register_form.username.data}!', 'success')
          # gets new user information from registration form and stores it in the database
          new_user = User(email=request.form.get('email_address'), first_name=request.form.get('first_name'), password=generate_password_hash(
          request.form.get('password'), method='sha256')) # hashes the password before it is stored for security
          db.session.add(new_user)
          db.session.commit()
          return redirect(url_for('auth.register'))
  return render_template("sign_up.html", title='Register', form=register_form)

@auth.route('/logout')
def logout():
  return '<p>Logout</p>'
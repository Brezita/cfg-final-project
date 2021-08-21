# authorisation routes
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, login_required, logout_user, current_user
from website import db, bcrypt
from website.models import User
from website.forms import RegistrationForm, LoginForm

# defining this file is a Blueprint of our application, it has a group of URL's

auth = Blueprint('auth', __name__)

# login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
  # checks if the user is logged in, if it is direct to the homepage
  if current_user.is_authenticated:
    return redirect(url_for('views.home'))
  login_form = LoginForm()
  if login_form.validate_on_submit():
    # checks to see if the user is in the database
    user = User.query.filter_by(email=login_form.email.data).first()
    if user:
      # checks password entered matches the stored hashed password 
      if bcrypt.check_password_hash(user.password, login_form.password.data):
        login_user(user, remember=login_form.remember.data)
        return redirect(url_for('views.home'))
      else:
        flash('Incorrect password. Please try again!', 'danger')
    else: 
      flash('User account does not exist. Please try again!', 'danger')
  return render_template('login.html', title='Login', form=login_form)

# registration route
@auth.route('/register', methods=['GET', 'POST'])
def register():
  # checks if the user is logged in, if it is direct to the homepage
  if current_user.is_authenticated:
    return redirect(url_for('views.home'))
  # creates an instance for the RegistrationForm class
  register_form = RegistrationForm()
  if register_form.validate_on_submit():
    # hashing the password to a string
    hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
    
    # creating new instance of user
    user = User(first_name=register_form.first_name.data, last_name=register_form.last_name.data, username=register_form.username.data, email=register_form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    
    # if successful display message and redirect user to login page
    flash(f'Your account has been created. You can now login!', 'success')
    return redirect(url_for('auth.login'))
  return render_template("sign_up.html", title='Register', form=register_form)

# logout route
@auth.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('views.home'))
# authorisation

from website.forms import RegistrationForm, LoginForm
from flask import Blueprint, render_template, url_for, flash, redirect
from .views import views

# defining this file is a Blueprint of our application, it has a group of URL's

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
  login_form = LoginForm()
  return render_template("login.html", title='Login', form=login_form, boolean=True)

@auth.route('/register', methods=['GET', 'POST'])
def register():
  # creates an instance
  register_form = RegistrationForm()
  if register_form.validate_on_submit():
    flash(f'Account created for {register_form.username.data}!', 'success')
    return redirect(url_for('auth.register'))
  return render_template("sign_up.html", title='Register', form=register_form)

@auth.route('/logout')
def logout():
  return '<p>Logout</p>'
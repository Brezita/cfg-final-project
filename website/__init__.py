# Setting up Flask Application
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Defining the database
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
  # represents the name of the file
  app = Flask(__name__) 
  # secures the cookies and session data related to the website
  app.config['SECRET_KEY'] = '1533e2ab57a4a84099e9ba68935b9d44'
  # links database to app
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)
  Session(app)
  
  # registering our Blueprint
  from .views import views
  from .auth import auth
  
  # registering with the Flask app
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  
  # db classes
  from .models import User, Note

  create_database(app)

  # authorises login
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))

  return app

# if database does not exist, create database
def create_database(app):
  if not path.exists('website/' + DB_NAME):
      db.create_all(app=app)
      print('Created Database!')

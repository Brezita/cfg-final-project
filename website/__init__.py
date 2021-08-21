# Setting up Flask Application
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()
db_name = "database.db"
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
  # represents the name of the file
  app = Flask(__name__) 
  # secures the cookies and session data related to the website
  app.config['SECRET_KEY'] = '1533e2ab57a4a84099e9ba68935b9d44'
  app.config["SESSION_TYPE"] = "filesystem"
  # links database to app
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
  # initialising the db
  db.init_app(app)
  # initialising the bycrpt
  bcrypt.init_app(app)
  # initialising the login_manager
  login_manager.init_app(app)
  Session(app)
  
  # registering our Blueprint
  from .views import views
  from .auth import auth
  
  # registering with the Flask app
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  
  # db class
  from website.models import User

  create_database(app)

  return app

# if database does not exist, create database
def create_database(app):
  if not path.exists('website/' + db_name):
      db.create_all(app=app)
      print('Database created')

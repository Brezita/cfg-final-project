# Setting up Flask Application
from flask import Flask
from flask_session import Session

def create_app():
  # represents the name of the file
  app = Flask(__name__) 
  # secures the cookies and session data related to the website
  app.config['SECRET_KEY'] = '1533e2ab57a4a84099e9ba68935b9d44'
  app.config["SESSION_TYPE"] = "filesystem"
  Session(app)
  
  # registering our Blueprint
  from .views import views
  from .auth import auth
  
  # registering with the Flask app
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  
  return app
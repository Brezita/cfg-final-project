# Database creation 
from . import db, login_manager
from flask_login import UserMixin

# finding the user by the user id
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# stores the user information into a table
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(150), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  
  # magic method - this sets how the User object will display in the command line
  def __repr__(self):
    return f"User('{self.username}','{self.email}')"
# create an application and run the application
from website import create_app

app = create_app()

# only run if you execute this file
if __name__ == '__main__': 
  app.run(debug=True) # stops us from re running flask all the time


  
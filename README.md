# Cloudtunes
Cloudtunes is a weather app that chooses music for users based on local weather.

## File Structure
### __app.py__
Creates an instance of the app.

### __website/\_\_init\_\_.py__
Defines the setup of the website package - this will be run on execution of the app.py file/instantiation of the app.

### __website/api_helpers.py__
Contains the functions that process the API requests - this includes making GET requests, acquiring authorisation tokens, and returning data to the main program.

### __website/auth.py__
Contains all of the server routes that handle authorsiation internally.

### __website/forms.py__
Contains the classes that correspond to, and handle the data from, the login and registration forms.

### __website/models.py__
Contains the classes that interface with the SQL database.

### __website/playlists.py__
Contains the classes that manage playlist and track data.

### __website/views.py__
Contains standard server routes (those that do not handle internal authentication).

### __website/static__
Contains static files - these are the CSS file and any images.

### __website/templates__
Contains HTML templates, including the layout template and templates for individual pages rendered in with Jinja.

### __tests/app_tests.py__
Contains the unit tests for the app.


## Requirements
Before running this code, you will need to have installed several Python packages. If you are using Python's pip, you can do this by executing the following commands:

`pip install Flask`\
`pip install spotipy`\
`pip install Flask-Session`\
`pip install WTForms`\
`pip install Flask-WTF`\
`pip install requests`\
`pip install flask_sqlalchemy`

Additionally, you will need to create an api_utils.py file, which should live in the 'website' directory. This should contain the API keys needed to run the app - this will include the getgeoapi.com API, the openweathermap.com API, and Spotify's client ID and client secret. CFG instructors: please message one of the project team to be sent a full set of keys.

## Usage
In order to run the code, you will need to navigate into the same directory as the app.py file, then execute one of the following commands in your terminal. This will launch the application, give the IP address at which the application is running, and allow you to open the application in your browser.

Using Bash:

```
export FLASK_APP=hello
flask run
```

Using Windows Powershell:
```
$env:FLASK_APP = "hello"
flask run
```

Using Windows CMD:
```
set FLASK_APP=hello
flask run
```

## Contributers
ASim-Null - Alexandra Simon-Lewis\
Brezita - Heather Cartwright\
jmdoherty1 - Johanna Doherty\
heyjulesb - Jules Luu\
kmh256 - Kara Howard

What we want, is to understand what each file in your repo is, how to run your code (even the link access is sort of running), what vanity to, how to interact with it. Things like that. I have not seen your code, what is all I need to understand it.
All this in nice, structured way, maybe some images not just text to show what's it about. Use markdown.
Hope this helps to at least get started with it.
Also, I know you do not need installing, we have not talked about that in class, but am I not supposed to interact/launch the website by running your main file?
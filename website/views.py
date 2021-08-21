# stores the URL end points for the front-end websites
# store standard routes - where the user can go to
from flask import Blueprint, render_template, redirect, request
from flask import session
from .api_helpers import get_user_location, get_user_weather, get_spotify_user_auth, call_spotify, get_user_playlists, get_spotify_token

# defining Blueprint
views = Blueprint('views', __name__)

# home page
@views.route("/", methods=['GET', 'POST'])
@views.route("/home", methods=['GET', 'POST'])
def home():
	location = get_user_location()
	weather = get_user_weather(location)
	playlist = call_spotify(weather)
	return render_template('index.html', playlist=playlist)

# about page
@views.route("/about")
def about():
	return render_template('about.html', title = 'About')

# playlist page
@views.route("/playlist")
def playlist_page():
  location = get_user_location()
  weather = get_user_weather(location)
  playlist = call_spotify(weather)
  return render_template('playlist.html', title = 'Playlist', playlist=playlist)

# Starts the Spotify authorisation process
@views.route("/spotify_login")
def spotify_login():
	username = "Brezita"
	auth_url = get_spotify_user_auth(session, username)

	if auth_url == 1:
		return redirect("/playlist")
	else:
		return redirect(auth_url)

# Completes the Spotify authorisation process and redirects user back to home
@views.route("/callback")
def spotify_callback():
  code = request.args.get("code")
  get_spotify_token(session, code)
  return redirect("/playlist")

# Not used - will eventually allow user playlists to be passed to template
@views.route("/user_playlists")
def user_playlists():
	return get_user_playlists(session)


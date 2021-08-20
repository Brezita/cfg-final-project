# stores the URL end points for the front-end websites
# store standard routes - where the user can go to

from flask import Blueprint, render_template, redirect, request, flash, jsonify
from flask_login import login_required, current_user
from flask_session import Session
from .models import Note
from . import db
import json
from .api_helpers import get_user_location, get_user_weather, get_spotify_user_auth, call_spotify, get_user_playlists, get_spotify_token
from .playlists import Playlist, Track

# defining Blueprint
views = Blueprint('views', __name__)

# home page
@views.route("/", methods=['GET', 'POST'])
@views.route("/home", methods=['GET', 'POST'])
def home():
	location = get_user_location()
	weather = get_user_weather(location)
	playlist = call_spotify(weather)
	if request.method == 'POST':
		note = request.form.get('note')
		if len(note) < 1:
			flash('Note is too short!', category='error')
		else:
			new_note = Note(data=note, user_id=current_user.id)
			db.session.add(new_note)
			db.session.commit()
			flash('Note added!', category='success')
		return render_template('index.html', user=current_user)

	return render_template('index.html', playlist=playlist)

# about page
@views.route("/about")
def about():
	return render_template('about.html', title = 'About')

# Starts the Spotify authorisation process
@views.route("/spotify_login")
def spotify_login():
	username = "Brezita"
	auth_url = get_spotify_user_auth(username)

	if auth_url == 1:
		return redirect("/")
	else:
		return redirect(auth_url)

# Completes the Spotify authorisation process and redirects user back to home
@views.route("/callback")
def spotify_callback():
  code = request.args.get("code")
  get_spotify_token(code)
  return redirect("/")


@views.route("/user_playlists")
def user_playlists():
	return get_user_playlists()

@views.route('/delete-note', methods=['POST'])
def delete_note():
	note = json.loads(request.data)
	noteId = note['noteId']
	note = Note.query.get(noteId)
	if note:
		if note.user_id == current_user.id:
			db.session.delete(note)
			db.session.commit()
	
	return jsonify({})

import requests
import json
import spotipy

from flask import session
from .api_utils import weather_api_key, geo_api_key, spot_client_id, spot_client_secret
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from .playlists import Playlist

def get_user_location():
    print("Getting user location")
    # Geolocation API - gets user location through IP address. 
    url_2 = "https://api.getgeoapi.com/v2/ip/check?api_key={}".format(geo_api_key)
    
    querystring = {"format":"json"}

    headers = {'x-rapidapi-host': 'ip-geo-location.p.rapidapi.com'}

    try:
        response = requests.request("GET", url_2, headers=headers, params=querystring)
        print(response)
        location_data = json.loads(response.text)
        return (location_data['location']['latitude'], location_data['location']['longitude'])
    except:
        print("Could not access geolocation API.")
        return "API error: geolocation API was not found."

# This needs to be rewritten to accommodate when location is entered as a place rather than lat/lon
def get_user_weather(location):
    # location[0] is latitute; location[1] is longitude
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric".format(location[0], location[1], weather_api_key)

    try:
        response = requests.get(url)
        print(response)
        data = json.loads(response.text)
        print(data)
        return(data['weather'][0]['main'])
    except:
        print("Could not access weather API.")
        return "API error: weather API was not found."

    # The following code has been taken out for the time being but left in incase it needs to be added back
            # # Found this difficult - until I added the zero. Hadn't noticed there was more than one item in 'main'. 
            # main = data['weather'][0]['main']
            # print(main)

            # temp = data['main']['temp']
            # print(f"Temperature is {temp} degrees celsius") #adjusted api url per documentation for metric units

            # #extra precision for more potential functions
            # extra_precision_ = data['weather'][0]['description']
            # humidity = data['main']['humidity']
            # wind = data['wind']['speed']
            # timezone = data['timezone']
            # icon = data['weather'][0]['icon']
            # #need to download icons for use if you want. probably get the music down first before that. 


# Authorisation flow for Spotify user
# Need to work out how to deal with this if it fails
def get_spotify_user_auth(username):
    try:
        sp = SpotifyOAuth(client_id=spot_client_id,
                            client_secret=spot_client_secret,
                            redirect_uri="http://127.0.0.1:5000/callback",
                            scope = 'user-library-read playlist-read-private',
                            username=username)
        session["spotify_user_auth"] = sp
        url = sp.get_authorize_url()
        return url
    except:
        print("Could not get authorisation.")
        return 1

# Second part of Spotify auth flow
def get_spotify_token(code):
    auth = session["spotify_user_auth"]
    try:
        auth.get_access_token(code=code)
    except:
        return 1
    return 0

# Split this out into two playlists - adding code and getting playlists should be separate
# Return user's playlists
def get_user_playlists():
    sp = spotipy.Spotify(oauth_manager=session["spotify_user_auth"])
    
    playlists = sp.current_user_playlists()
    print(playlists)
    return playlists

# Return music based on current weather
def call_spotify(query):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spot_client_id,
                                                            client_secret=spot_client_secret))
        results = sp.search(q=query, limit=20)

        playlist = Playlist(query)
        for item in results['tracks']['items']:
            if item['explicit'] == False:
                track = playlist.Track(item['name'], [artist['name'] for artist in item['artists']], item['id'], item['duration_ms'], item['external_urls']['spotify'])
                playlist.addTrack(track)

        return playlist
    except:
        return "Could not get Spotify playlist :("
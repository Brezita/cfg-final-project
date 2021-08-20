import requests
import json
import spotipy

from .api_utils import weather_api_key, geo_api_key, spot_client_id, spot_client_secret
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from .playlists import Playlist

GEO_API = {
    "url": "https://api.getgeoapi.com/v2/ip/check",
    "querystring": {"format":"json"},
    "headers": {'x-rapidapi-host': 'ip-geo-location.p.rapidapi.com'}
}

WEATHER_API = {
    "url": "https://api.openweathermap.org/data/2.5/weather"
}


def get_user_location():
    ''' Geolocation API - gets user location through IP address. '''
    response = get_api_response(GEO_API["url"] + "?api_key={}".format(geo_api_key), headers=GEO_API["headers"], querystring=GEO_API["querystring"])
    
    try:
        location_data = json.loads(response.text)
        return (location_data['location']['latitude'], location_data['location']['longitude'])
    except:
        print("Could not access geolocation API.")
        return "API error: geolocation API was not found."

# This will eventually need to be rewritten to accommodate when location is entered as a place rather than lat/lon
def get_user_weather(location):
    ''' Open Weather API - gets user weather using location. '''
    # location[0] is latitute; location[1] is longitude
    response = get_api_response(WEATHER_API['url'] + "?lat={}&lon={}&appid={}&units=metric".format(location[0], location[1], weather_api_key))

    try:
        data = json.loads(response.text)
        
        # stores location
        Playlist.PlaylistLocationData.location = data['name']
        Playlist.PlaylistLocationData.country = data['sys']['country']
        
        # stores weather description
        Playlist.PlaylistLocationData.weather = data['weather'][0]['description']
        
        return(data['weather'][0]['main'])
    except:
        print("Could not access weather API.")
        return "API error: weather API was not found."

def get_api_response(url, **kwargs):
    ''' Mostly does the job of requests.get, but with added error handling. '''
    response = requests.get(url, kwargs)
    if response.ok:
        return response
    else:
        return None

# Authorisation flow for Spotify user
def get_spotify_user_auth(mysession, username):
    try:
        sp = SpotifyOAuth(client_id=spot_client_id,
                            client_secret=spot_client_secret,
                            redirect_uri="http://127.0.0.1:5000/callback",
                            scope = 'user-library-read playlist-read-private',
                            username=username)
        mysession["spotify_user_auth"] = sp
        url = sp.get_authorize_url()
        return url
    except:
        print("Could not get authorisation.")
        return 1

# Second part of Spotify auth flow
def get_spotify_token(mysession, code):
    auth = mysession["spotify_user_auth"]
    try:
        auth.get_access_token(code=code)
    except:
        print("Could not get token.")
        return 1
    print("Got token, returning.")
    return 0

# Split this out into two playlists - adding code and getting playlists should be separate
# Return user's playlists
def get_user_playlists(mysession):
    sp = spotipy.Spotify(oauth_manager=mysession["spotify_user_auth"])
    
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

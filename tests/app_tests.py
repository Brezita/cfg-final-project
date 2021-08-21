import unittest

import json

from app import app
from website.api_helpers import get_api_response, get_user_weather, get_spotify_user_auth, get_user_playlists
from website.playlists import Playlist


class TestGetApiResponse(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.url = "https://cloudtunes.free.beeceptor.com"

    # Tests that the correct OK response is returned
    def test_ok_response(self):
        response = get_api_response(self.url + "/ok_response")
        self.assertTrue(response.ok)

    # Tests that the correct response is returned when API call fails
    def test_404_response(self):
        response = get_api_response(self.url + "/not_ok_response")
        self.assertEqual(response, None)

class TestGetUserWeather(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.possible_weather = ["Thunderstorm", "Drizzle", "Rain", "Snow", "Clear", "Clouds", "Mist", 
                            "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash", "Squall", "Tornado"]
 
    # Tests that function behaves correctly with location provided
    def test_with_location(self):
        location = (51.3178, -0.5724)
        result = get_user_weather(location)
        self.assertIn(result, self.possible_weather)

    # Tests that function behaves correctly when location call fails
    def test_with_location_failure(self):
        input = "API error: geolocation API was not found."
        result = get_user_weather(input)
        self.assertEqual(result, "API error: weather API was not found.")

class TestGetSpotifyUserAuth(unittest.TestCase):
    # Tests function success
    def test_get_auth(self):
        username = "Brezita"
        result = get_spotify_user_auth(dict(), username)
        self.assertEqual(result[0:5], "https")

    # Tests function failure by not providing session variable
    def test_auth_failure(self):
        username = "Brezita"
        result = get_spotify_user_auth(None, username)
        self.assertEqual(result, 1)

class PlaylistsTest(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        with open("tests/spotify_track_data.json", "r+") as myfile:
            spotify_data = myfile.read()
            spotify_data = json.loads(spotify_data)
        self.playlist = Playlist("Clouds")
        for item in spotify_data['tracks']['items']:
            track = self.playlist.Track(item['name'], [artist['name'] for artist in item['artists']], item['id'], item['duration_ms'], item['external_urls']['spotify'])
            self.playlist.addTrack(track)

    # Tests getting the second track from the first
    def test_get_next_track(self):
        next_song = self.playlist.changeTrack("next")
        self.assertEqual(next_song.title, "JUST LIKE YOU")

    # Tests getting the first track from the last
    def test_return_to_first_track(self):
        self.playlist.current_track = len(self.playlist.tracks) - 1
        next_song = self.playlist.changeTrack("next")
        self.assertEqual(next_song.title, "CLOUDS")

    # Tests getting the first track from the second
    def test_get_previous_track(self):
        self.playlist.current_track = 1
        previous_song = self.playlist.changeTrack("previous")
        self.assertEqual(previous_song.title, "CLOUDS")

    # Tests getting the last track from the first
    def test_return_to_last_track(self):
        previous_song = self.playlist.changeTrack("previous")
        self.assertEqual(previous_song.title, "Clouds as Witnesses")
        
    # Tests that the tracks have actually shuffled
    def test_tracks_shuffled(self):
        unshuffled_playlist = self.playlist.tracks
        self.playlist.shuffleTracks()
        self.assertNotEqual(unshuffled_playlist, self.playlist.tracks)
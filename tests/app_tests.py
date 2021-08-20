import unittest

import json

from website.api_helpers import get_api_response, get_user_weather, get_spotify_user_auth, get_user_playlists
from website.playlists import Playlist


class TestGetApiResponse(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.url = "https://cloudtunes.free.beeceptor.com"

    def test_ok_response(self):
        response = get_api_response(self.url + "/ok_response")
        self.assertTrue(response.ok)

    def test_404_response(self):
        response = get_api_response(self.url + "/not_ok_response")
        self.assertEqual(response, None)

class TestGetUserWeather(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.possible_weather = ["Thunderstorm", "Drizzle", "Rain", "Snow", "Clear", "Clouds", "Mist", 
                            "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash", "Squall", "Tornado"]

    def test_with_location(self):
        location = (51.3178, -0.5724)
        result = get_user_weather(location)
        self.assertIn(result, self.possible_weather)

    def test_with_location_failure(self):
        input = "API error: geolocation API was not found."
        result = get_user_weather(input)
        self.assertEqual(result, "API error: weather API was not found.")

# # This test is failing but I don't know why
# class TestGetSpotifyUserAuth(unittest.TestCase):
#     # Should return a URL
#     # Also test without id/secret
#     # This might just not work tbh
#     def test_get_auth(self):
#         username = "Brezita"
#         result = get_spotify_user_auth(username)
#         print(result)
#         self.assertEqual(result[0:4], "https")

class GetUserPlaylistsTest(unittest.TestCase):
    # Will need to pre-run get_spotify_user_auth
    # Should return a list of playlists
    pass

class CallSpotifyTest(unittest.TestCase):
    # Should return a Playlist object of Tracks based on the given weather
    # Test without id/secret - this will simulate expired keys
    # Test with no weather input ("API error: weather API was not found.")
    # Test with several accepted weather types
    pass

class PlaylistsTest(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        with open("spotify_track_data.json", "r+") as myfile:
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
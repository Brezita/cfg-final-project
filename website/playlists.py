import random

# This class is underused, but will eventually be used to manipulate playlists
# A few examples of methods we think will be useful are given
class Playlist:
# Handles passing of playlist data
    def __init__(self, title):
        self.title = title
        self.tracks = []
        self.current_track = 0
        self.total_tracks = -1
    
    # Append a new track to the end of the playlist
    def addTrack(self, newtrack):
        self.tracks.append(newtrack)
        self.total_tracks += 1

    # Change track (<| or |> buttons)
    def changeTrack(self, direction):
        if direction == "next":
            if self.current_track < self.total_tracks:
                self.current_track += 1
            elif self.current_track == self.total_tracks:
                self.current_track = 0
            else:
                print("No tracks found.")
        elif direction == "previous":
            if self.current_track > 0:
                self.current_track -= 1
            elif self.current_track == 0:
                self.current_track = self.total_tracks
            else:
                print("No tracks found.")
        return self.tracks[self.current_track]

    # Reorders the playlist
    def shuffleTracks(self):
        self.tracks = random.shuffle(self.tracks)

    # Deletes the playlist
    def emptyPlaylist(self):
        self.__del__()

    # Handles individual tracks
    class Track:
        def __init__(self, title, artist, spotifyid, duration, url):
            self.title = title
            self.artist = artist
            self.spotifyid = spotifyid
            self.duration = duration
            self.url = url    

    # Handles playlist metadata - what was happening when this was generated?
    class PlaylistLocationData:
        def __init__(self, location, country, weather):
            self.location = location
            self.country = country
            self.weather = weather

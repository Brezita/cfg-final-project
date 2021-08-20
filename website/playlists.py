import random

class Playlist:
    class Track:
        def __init__(self, title, artist, spotifyid, duration, url):
            self.title = title
            self.artist = artist
            self.spotifyid = spotifyid
            self.duration = duration
            self.url = url

        def getDuration(self):
            return self.duration

    def __init__(self, title):
        self.title = title
        self.tracks = []
        self.current_track = 0
        self.total_tracks = -1
    
    def addTrack(self, newtrack):
        self.tracks.append(newtrack)
        self.total_tracks += 1

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

    def shuffleTracks(self):
        self.tracks = random.shuffle(self.tracks)

    def removeForever(self):
        pass

    def emptyPlaylist(self):
        self.__del__()
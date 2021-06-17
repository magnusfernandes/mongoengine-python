from spotify.models import SpotifyAPI
from spotify.resources import SpotifyResources
from flask import Flask
from mongoengine import connect
from api.genres.resources import GenreResources
from api.languages.resources import LanguageResources
from api.artists.resources import ArtistResources
from api.contents.resources import ContentResources
from api.events.resources import EventResources
from api.playlists.resources import PlaylistResources
from api.users.resources import UserResources

app = Flask(__name__)

# Database
DBNAME = "python_test"
DBURI = "mongodb://localhost:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000"
connect(db=DBNAME, host=DBURI)

# Dump from spotify
clientId = "bdcca20ecf894d0b99fdc786c58aab42"
clientSecret = "c3c3d4822537434c97a9a5f1ffbded8b"

spotify = SpotifyAPI(clientId, clientSecret)
spotify.performAuth()
print("Spotify access token:", spotify.getAccessToken())
SpotifyResources(accessToken=spotify.getAccessToken())
# SpotifyResources.fetchPlaylists()


# Seed data
# genres = GenreResources.DumpGenres()
# languages = LanguageResources.DumpLanguages()
# artist = ArtistResources.createArtist(language=languages[0])
# content = ContentResources.createContent(
#     forArtist=artist, language=languages[0], genre=genres[0])
# event = EventResources.createEvent(forArtist=artist)
# users = UserResources.DumpUsers()
# playlist = PlaylistResources.createNewPlaylist(
#     forUser=users[0], content=content)

# print("Database seeded successfully")

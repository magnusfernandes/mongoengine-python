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

# Seed data
genres = GenreResources.DumpGenres()
languages = LanguageResources.DumpLanguages()
artist = ArtistResources.createArtist(language=languages[0])
content = ContentResources.createContent(
    forArtist=artist, language=languages[0], genre=genres[0])
event = EventResources.createEvent(forArtist=artist)
users = UserResources.DumpUsers()
playlist = PlaylistResources.createNewPlaylist(
    forUser=users[0], content=content)

print("Database seeded successfully")

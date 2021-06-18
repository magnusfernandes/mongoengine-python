from spotify.models import SpotifyAPI
from spotify.resources import SpotifyResources
from flask import Flask
from mongoengine import connect

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

print("Database seeded successfully")
exit()

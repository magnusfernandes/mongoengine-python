from api.artists.models import Artists
from api.languages.models import Languages
from api.genres.models import Genres
import requests
from urllib.parse import urlencode
from faker import Faker
from faker.providers import internet, misc
from random import randrange

from api.playlists.models import PlayList
from api.users.models import Users


class SpotifyResources(object):
    accessToken = ""
    users = []
    genres = []
    playlists = []
    languages = []
    artists = []

    def __init__(self, accessToken):
        super().__init__()
        self.accessToken = accessToken
        self.createUsers()
        self.createGenres()
        self.createLanguages()
        for idx in range(0, 199):
            self.createArtists(offset=idx)
        # for idx in range(0, 159):
        # self.createSongs(offset=0)

    def getHeader(self):
        headers = {
            "Authorization": f"Bearer {self.accessToken}"
        }
        return headers

    def createUsers(self):
        fake = Faker(internet)
        for _ in range(100):
            user = Users(
                name=fake.name(),
                email=fake.ascii_company_email()
            ).save()
            self.users.append(user)

    def createGenres(self):
        endpoint = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
        resp = requests.get(endpoint, headers=self.getHeader())
        respData = resp.json()
        allGenres = respData['genres']
        for idx, genre in enumerate(allGenres):
            genre = Genres(
                name=genre,
                profilePic=f"https://picsum.photos/id/{idx}/200/200"
            ).save()
            self.genres.append(genre)

    def createLanguages(self):
        languages = ["English", "Hindi", "Bengali", "Marathi",
                     "Telugu", "Tamil", "Gujarati", "Urdu", "Kannada", "Malayalam"]
        for item in languages:
            language = Languages(
                name=item
            ).save()
            self.languages.append(language)

    def createArtists(self, offset):
        fake = Faker(misc)
        url = "https://api.spotify.com/v1/search"
        data = {
            "q": "a",
            "type": "artist",
            "limit": 50,
            "offset": offset
        }
        endpoint = f"{url}?{urlencode(data)}"
        resp = requests.get(endpoint, headers=self.getHeader())
        respData = resp.json()
        artistsData = respData['artists']['items']
        for data in artistsData:
            languages = []
            for _ in range(0, randrange(9)):
                languages.append(self.languages[randrange(9)])
            genres = []
            for _ in range(0, randrange(len(self.genres))):
                genres.append(self.genres[randrange(len(self.genres))])
            profileImg = None
            if len(data['images']) > 0:
                profileImg = data['images'][0]['url']
            artist = Artists(
                firstName=data['name'],
                lastName=fake.last_name(),
                profilePicture=profileImg,
                featuredPictureUrl=profileImg,
                bio=fake.paragraph(nb_sentences=3),
                languages=languages,
                genres=genres,
                coreMember=fake.boolean(chance_of_getting_true=25),
                verifiedMember=fake.boolean(chance_of_getting_true=50)
            ).save()
            self.artists.append(artist)

    def createSongs(self, offset):
        url = "https://api.spotify.com/v1/search"
        data = {
            "q": "a",
            "type": "track",
            "limit": 50,
            "offset": offset
        }
        endpoint = f"{url}?{urlencode(data)}"
        resp = requests.get(endpoint, headers=self.getHeader())
        respData = resp.json()
        print(respData)

    def createPlaylist(self, playlists):
        for idx, data in enumerate(playlists):
            images = data['images']
            if len(images) == 0:
                images = [
                    {
                        "url": f"{randrange(1000)}"
                    }
                ]
            thumbnails = []
            for img in images:
                thumbnails.append(img['url'])
            playlist = PlayList(
                title=data['name'],
                description=data['description'],
                curated=True,
                user=self.users[idx % 100],
                language=data['name'],
                genre=data['name'],
                contents=data['name'],
                thumbnailUrl=thumbnails,
                featuredPictureUrl=images[0]['url'],
                totalLikes=randrange(20, 1000),
                totalViews=randrange(900, 1000000)
            )
        return playlist

    def fetchPlaylists(self):
        url = "https://api.spotify.com/v1/search"
        data = {
            "q": "a",
            "type": "playlist",
            "limit": 50
        }
        endpoint = f"{url}?{urlencode(data)}"
        resp = requests.get(endpoint, headers=self.getHeader())
        respData = resp.json()
        playlists = respData['playlists']['items']
        self.createPlaylist(playlists)

import requests
from faker import Faker
from random import randrange
from urllib.parse import urlencode
from rich import console, progress

from api.playlists.models import PlayList
from api.users.models import Users
from api.events.models import Events
from api.contents.models import ContentGroups, ContentType, Contents
from api.artists.models import Artists
from api.languages.models import Languages
from api.genres.models import Genres

console = console.Console()


class SpotifyResources(object):
    accessToken = ""
    users = []
    genres = []
    languages = []
    artists = []
    tracks = []
    events = []
    episodes = []
    playlists = []
    podcasts = []
    albums = []

    def __init__(self, accessToken):
        super().__init__()
        self.accessToken = accessToken
        self.createUsers()
        console.print("Users loaded!", style="bold red")
        self.createGenres()
        console.print("Genres loaded!", style="bold red")
        self.createLanguages()
        console.print("Languages loaded!", style="bold red")
        for idx in progress.track(range(0, 200), description="[bold red]Loading artists"):
            self.createArtists(offset=idx)
        self.createAlbums()
        console.print("Albums loaded!", style="bold red")
        for idx in progress.track(range(0, 160), description="[bold red]Loading tracks"):
            self.createSongs(offset=idx)
        for idx in progress.track(range(0, 100), description="[bold red]Loading podcasts"):
            self.createPodcasts()
        self.fetchPlaylists()
        console.print("Playlists loaded!", style="bold red")
        self.createEvents()
        console.print("Events loaded!", style="bold red")

    def getHeader(self):
        headers = {
            "Authorization": f"Bearer {self.accessToken}"
        }
        return headers

    def createUsers(self):
        fake = Faker()
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
            newGenre = Genres(
                name=genre,
                profilePic=f"https://picsum.photos/id/{idx}/200/200"
            ).save()
            self.genres.append(newGenre)

    def getRandomGenreList(self):
        genres = []
        for _ in range(0, randrange(3)):
            genres.append(self.genres[randrange(len(self.genres))])
        return genres

    def createLanguages(self):
        languages = ["English", "Hindi", "Bengali", "Marathi",
                     "Telugu", "Tamil", "Gujarati", "Urdu", "Kannada", "Malayalam"]
        for item in languages:
            language = Languages(
                name=item
            ).save()
            self.languages.append(language)

    def getRandomLanguageList(self):
        languages = []
        for _ in range(0, randrange(5)):
            languages.append(self.languages[randrange(len(self.languages))])
        return languages

    def createArtists(self, offset):
        fake = Faker()
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
            profileImg = None
            if len(data['images']) > 0:
                profileImg = data['images'][0]['url']
            artist = Artists(
                firstName=data['name'],
                lastName=fake.last_name(),
                profilePicture=profileImg,
                featuredPictureUrl=profileImg,
                bio=fake.paragraph(nb_sentences=3),
                languages=self.getRandomLanguageList(),
                genres=self.getRandomGenreList(),
                coreMember=fake.boolean(chance_of_getting_true=25),
                verifiedMember=fake.boolean(chance_of_getting_true=50)
            ).save()
            self.artists.append(artist)

    def getRandomArtistList(self):
        artists = []
        for _ in range(0, randrange(5)):
            artists.append(self.artists[randrange(len(self.artists))])
        return artists

    def getRandomArtist(self):
        return self.artists[randrange(len(self.artists))]

    def createSongs(self, offset):
        fake = Faker()
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
        tracksData = respData['tracks']['items']
        for data in tracksData:
            images = []
            for img in data['album']['images']:
                images.append(img['url'])
            featured = None
            if len(images) > 0:
                featured = images[0]
            track = Contents(
                title=data['name'],
                description=fake.paragraph(nb_sentences=2),
                language=self.getRandomLanguageList(),
                contentType=ContentType.Music,
                genre=self.genres[randrange(len(self.genres))],
                leadArtist=self.getRandomArtist(),
                credits=fake.paragraph(nb_sentences=12),
                lyricsUrl=fake.url(),
                audioUrl=fake.url(),
                subTitlesUrl=fake.url(),
                videoUrl=fake.url(),
                thumbnailUrl=images,
                featuredPictureUrl=featured,
                totalLikes=randrange(20, 10000),
                totalViews=randrange(900, 1000000)
            ).save()
            self.tracks.append(track)

    def getRandomTracksList(self):
        tracks = []
        for _ in range(0, randrange(5)):
            tracks.append(self.tracks[randrange(len(self.tracks))])
        return tracks

    def createPodcasts(self):
        fake = Faker()
        podcast = ContentGroups(
            title=fake.name(),
            description=fake.paragraph(nb_sentences=3),
            contentType=ContentType.Podcast,
            totalLikes=randrange(20, 1000),
            totalViews=randrange(900, 1000000)
        ).save()
        self.podcasts.append(podcast)
        self.createEpisodesForPodcast(podcast=podcast)

    def createEpisodesForPodcast(self, podcast):
        fake = Faker()
        url = "https://api.spotify.com/v1/search"
        data = {
            "q": fake.random_element(elements=('a', 'e', 'i', 'o', 'u')),
            "type": "episode",
            "limit": 10,
            "offset": randrange(0, 10),
            "market": "US"
        }
        endpoint = f"{url}?{urlencode(data)}"
        resp = requests.get(endpoint, headers=self.getHeader())
        respData = resp.json()
        episodesData = respData['episodes']['items']
        for data in episodesData:
            images = []
            for img in data['images']:
                images.append(img['url'])
            featured = None
            if len(images) > 0:
                featured = images[0]
            track = Contents(
                title=data['name'],
                description=data['description'],
                language=self.getRandomLanguageList(),
                contentType=ContentType.Episode,
                contentGroup=podcast,
                videoUrl=fake.url(),
                thumbnailUrl=images,
                featuredPictureUrl=featured,
                totalLikes=randrange(20, 10000),
                totalViews=randrange(900, 1000000)
            ).save()
            self.episodes.append(track)

    def createEvents(self):
        fake = Faker()
        url = "https://api.spotify.com/v1/search"
        data = {
            "q": "i",
            "type": "show",
            "limit": 20,
            "market": "IN"
        }
        endpoint = f"{url}?{urlencode(data)}"
        resp = requests.get(endpoint, headers=self.getHeader())
        respData = resp.json()
        showsData = respData['shows']['items']
        for data in showsData:
            images = []
            for img in data['images']:
                images.append(img['url'])
            featured = None
            if len(images) > 0:
                featured = images[0]
            event = Events(
                title=data['name'],
                description=data['description'],
                artists=self.getRandomArtistList(),
                maxParticipants=randrange(20, 10000),
                eventAt=fake.date_between(start_date='today', end_date='+1y'),
                eventDuration=randrange(20, 36000),
                eventLink=fake.url(),
                eventCost=randrange(100, 3000),
                thumbnailUrl=images,
                featuredPictureUrl=featured,
            ).save()
            self.events.append(event)

    def createAlbums(self):
        url = "https://api.spotify.com/v1/search"
        data = {
            "q": "i",
            "type": "album",
            "limit": 50,
            "market": "IN"
        }
        endpoint = f"{url}?{urlencode(data)}"
        resp = requests.get(endpoint, headers=self.getHeader())
        respData = resp.json()
        albumsData = respData['albums']['items']
        for data in albumsData:
            images = []
            for img in data['images']:
                images.append(img['url'])
            featured = None
            if len(images) > 0:
                featured = images[0]
            album = ContentGroups(
                title=data['name'],
                contentType=ContentType.Album,
                leadArtist=self.getRandomArtist(),
                thumbnailUrl=images,
                featuredPictureUrl=featured,
                totalLikes=randrange(20, 1000),
                totalViews=randrange(900, 1000000)
            ).save()
            self.albums.append(album)

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
                language=self.getRandomLanguageList(),
                genre=self.getRandomGenreList(),
                contents=self.getRandomTracksList(),
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

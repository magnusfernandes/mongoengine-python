from .models import Artists
from api.languages.models import Languages


class ArtistResources():
    def createArtist(language: Languages):
        artist = Artists(
            firstName="Ed",
            lastName="Sheeran",
            profilePicture="https://i.pravatar.cc/150?img=12",
            featuredPictureUrl="https://i.pravatar.cc/150?img=12",
            socialLinks=["https://i.pravatar.cc/150?img=12"],
            bio="Artist's bio",
            languages=[language],
            genres=[],
            coreMember=True,
            verifiedMember=True
        ).save()
        return artist

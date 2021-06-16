from .models import PlayList
from api.users.models import Users
from api.contents.models import Contents


class PlaylistResources():
    def createNewPlaylist(forUser: Users, content: Contents):
        playlist = PlayList(
            title="All time favorites",
            user=forUser,
            curated=False,
            contents=[content],
            totalLikes=400,
            totalViews=1200
        ).save()

        return playlist

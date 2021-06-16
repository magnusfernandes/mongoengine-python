from api.genres.models import Genres
from api.languages.models import Languages
from api.artists.models import Artists
from .models import ContentGroups, Contents


class ContentResources():
    def createContent(forArtist: Artists, language: Languages, genre: Genres):
        group = ContentGroups(
            title="Content group",
            description="Content group description",
            leadArtist=forArtist,
            thumbnailUrl=["https://i.pravatar.cc/150?img=12"],
            promoVideoUrl=["https://i.pravatar.cc/150?img=12"],
            promoAudioUrl=["https://i.pravatar.cc/150?img=12"],
            featuredPictureUrl="https://i.pravatar.cc/150?img=12",
            tags=["rap", "classical"],
            totalLikes=12,
            totalViews=24
        ).save()

        content = Contents(
            title="Test content",
            description="Content bio",
            language=[language],
            genre=genre,
            contentGroup=group,
            leadArtist=forArtist,
            credits="Test credits",
            lyricsUrl="https://i.pravatar.cc/150?img=12",
            audioUrl="https://i.pravatar.cc/150?img=12",
            subTitlesUrl="https://i.pravatar.cc/150?img=12",
            videoUrl="https://i.pravatar.cc/150?img=12",
            tags=[],
            thumbnailUrl=["https://i.pravatar.cc/150?img=12"],
            promoVideoUrl=["https://i.pravatar.cc/150?img=12"],
            promoAudioUrl=["https://i.pravatar.cc/150?img=12"],
            featuredPictureUrl="https://i.pravatar.cc/150?img=12",
            totalLikes=31,
            totalViews=2
        ).save()

        return content

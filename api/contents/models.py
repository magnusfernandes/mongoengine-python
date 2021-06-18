import enum
from mongoengine import (
    Document,
    StringField,
    ListField,
    IntField,
    ReferenceField,
    EmbeddedDocumentField,
    DateTimeField,
    EmbeddedDocument
)
from datetime import datetime

from api.genres.models import Genres
from api.artists.models import Artists
from api.languages.models import Languages


class ContentType(enum.IntEnum):
    Music = 1
    Podcast = 2
    Poetry = 3
    Episode = 4
    Album = 5


class ArtistCollaboration(EmbeddedDocument):
    title = StringField(max_length=256, required=True)


class ContentGroups(Document):
    title = StringField(max_length=256, required=True)
    description = StringField(max_length=256, required=False)
    contentType = IntField(choices=list(map(int, ContentType)),
                           default=ContentType.Music, required=True)
    leadArtist = ReferenceField(Artists, required=False)
    collobarators = ListField(EmbeddedDocumentField(
        ArtistCollaboration), required=False)
    thumbnailUrl = ListField(StringField(max_length=256, required=False))
    promoVideoUrl = ListField(StringField(max_length=256, required=False))
    promoAudioUrl = ListField(StringField(max_length=256, required=False))
    featuredPictureUrl = StringField(max_length=256, required=False)
    tags = ListField(StringField(max_length=256, required=False))
    totalLikes = IntField(default=0, required=True)
    totalViews = IntField(default=0, required=True)
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'contentGroups'
    }


class Contents(Document):
    title = StringField(max_length=256, required=True)
    description = StringField(max_length=4096, required=False)
    language = ListField(ReferenceField(Languages), required=False)
    contentType = IntField(choices=list(map(int, ContentType)),
                           default=ContentType.Music, required=True)
    genre = ReferenceField(Genres, required=False)
    contentGroup = ReferenceField(ContentGroups, required=False)
    leadArtist = ReferenceField(Artists, required=False)
    collobarators = ListField(EmbeddedDocumentField(
        ArtistCollaboration), required=False)
    credits = StringField(max_length=2048, required=False)
    lyricsUrl = StringField(max_length=256, required=False)
    audioUrl = StringField(max_length=256, required=False)
    subTitlesUrl = StringField(max_length=256, required=False)
    videoUrl = StringField(max_length=256, required=False)
    tags = ListField(StringField(max_length=256, required=False))
    thumbnailUrl = ListField(StringField(max_length=256, required=False))
    promoVideoUrl = ListField(StringField(max_length=256, required=False))
    promoAudioUrl = ListField(StringField(max_length=256, required=False))
    featuredPictureUrl = StringField(max_length=256, required=False)
    totalLikes = IntField(default=0, required=True)
    totalViews = IntField(default=0, required=True)
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)

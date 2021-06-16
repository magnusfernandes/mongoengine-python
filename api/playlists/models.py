from mongoengine import (
    Document,
    StringField,
    BooleanField,
    ReferenceField,
    ListField,
    DateTimeField,
    IntField
)
from datetime import datetime
from api.contents.models import Contents
from api.genres.models import Genres
from api.users.models import Users
from api.languages.models import Languages


class PlayList(Document):
    title = StringField(max_length=256, required=True)
    description = StringField(max_length=256, required=False)
    curated = BooleanField(Default=False, required=True)
    user = ReferenceField(Users, required=True)
    tags = ListField(StringField(max_length=256, required=False))
    language = ListField(ReferenceField(Languages), required=False)
    genre = ListField(ReferenceField(Genres), required=False)
    contents = ListField(ReferenceField(Contents), required=True)
    thumbnailUrl = ListField(StringField(max_length=256, required=False))
    featuredPictureUrl = StringField(max_length=256, required=False)
    totalLikes = IntField(default=0, required=True)
    totalViews = IntField(default=0, required=True)
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'playlist'
    }

from mongoengine import (
    Document,
    DateTimeField,
    StringField,
    ListField,
    ReferenceField,
    BooleanField
)
from datetime import datetime
from api.genres.models import Genres
from api.languages.models import Languages


class Artists(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    firstName = StringField(max_length=256, required=True)
    lastName = StringField(max_length=256, required=True)
    profilePicture = StringField(max_length=256, required=False)
    featuredPictureUrl = StringField(max_length=256, required=False)
    socialLinks = ListField(StringField(max_length=256))
    bio = StringField(max_length=2048, required=False)
    languages = ListField(ReferenceField(Languages), required=False)
    genres = ListField(ReferenceField(Genres), required=False)
    coreMember = BooleanField(required=True, default=False)
    verifiedMember = BooleanField(required=True, default=False)

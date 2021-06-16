import enum
from mongoengine import (
    Document,
    StringField,
    IntField,
    ListField,
    DateTimeField,
    ReferenceField
)
from datetime import datetime

from api.artists.models import Artists


class EventTypes(enum.IntEnum):
    Chat = 1


class Events(Document):
    title = StringField(max_length=256, required=True)
    description = StringField(max_length=256, required=False)
    eventType = IntField(choices=list(map(int, EventTypes)),
                         default=EventTypes.Chat, required=True)
    artists = ListField(ReferenceField(Artists), required=False)
    maxParticipants = IntField(default=50, required=False)
    eventAt = DateTimeField(default=datetime.now)
    eventDuration = IntField(default=50, required=False)
    eventLink = StringField(max_length=256, required=False)
    eventCost = IntField()
    thumbnailUrl = ListField(StringField(max_length=256, required=False))
    promoVideoUrl = ListField(StringField(max_length=256, required=False))
    promoAudioUrl = ListField(StringField(max_length=256, required=False))
    featuredPictureUrl = StringField(max_length=256, required=False)
    tags = ListField(StringField(max_length=256, required=False))

    meta = {
        "indexes": ["eventType"],
        "ordering": ["-eventAt"]
    }

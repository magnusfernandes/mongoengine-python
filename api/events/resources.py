from api.events.models import Events
from api.artists.models import Artists


class EventResources():
    def createEvent(forArtist: Artists):
        event = Events(
            title="New Year's Eve",
            description="New Year Party",
            artists=[forArtist],
            maxParticipants=200,
            eventDuration=90,
            eventLink="http://hoohle.com",
            eventCost=250,
            thumbnailUrl=["http://hoohle.com"],
            promoVideoUrl=["http://hoohle.com"],
            promoAudioUrl=["http://hoohle.com"],
            featuredPictureUrl="http://hoohle.com",
        ).save()
        return event

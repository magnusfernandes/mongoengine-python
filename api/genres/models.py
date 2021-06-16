from mongoengine import Document, StringField


class Genres(Document):
    name = StringField(max_length=256, required=True)
    profilePic = StringField(max_length=256, required=False)

from mongoengine import Document, StringField


class Languages(Document):
    name = StringField(max_length=256, required=True)

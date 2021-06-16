from enum import unique
from mongoengine import Document, StringField


class Users(Document):
    name = StringField(max_length=256, required=True)
    email = StringField(max_length=256, unique=True, required=True)

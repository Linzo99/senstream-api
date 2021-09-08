from mongoengine import *


class Channel(Document):
    _id = StringField(primary_key=True)
    name = StringField(required=True)
    thumbnails = ListField(DictField(), required=True)
    link = URLField(required=True)

    meta = {'collection' : 'channels' }
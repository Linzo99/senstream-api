from mongoengine import *

class Video(Document):
    _id = StringField(primary_key=True)
    title = StringField(required=True)
    thumbnails = ListField(DictField(), required=True)
    viewCount = IntField()
    description = StringField()
    rating = FloatField()
    published = StringField()
    uploaded = StringField()
    duration = StringField(required=True)
    link = URLField(required=True)
    playlist = StringField(required=True)
    channel = StringField(required=True)
    keywords = ListField()

    meta = {'collection' : 'videos'}
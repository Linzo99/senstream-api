from mongoengine import *

class Playlist(Document):
    _id = StringField(primary_key=True)
    title = StringField(required=True)
    videoCount = IntField()
    viewCount = IntField()
    thumbnails = ListField(DictField(), required=True)
    link = URLField(required=True)
    channel = StringField(required=True)

    meta = {'collection' : 'playlists'}
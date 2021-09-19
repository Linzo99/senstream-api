from mongoengine import connect
from .models.Playlist import Playlist
from .constants import PROVIDERS, collections, dbName
from .extractor import Extractor
from .util import Util


class Scraper:
    """ Class for scraping playlist videos """
    def __init__(self):
        self._util = Util()

    def scrape(self):
        connect(dbName)
        playlists = Playlist.objects.all()
        if len(playlists) > len(PROVIDERS):
            for provider in playlists:
                try:
                    extractor = Extractor(provider.title, provider.link)
                    extractor._getAllVideos()
                    for col in collections : self._util.exportCollection(col) 
                except Exception as e:
                    print(e)
        else:
            for provider in PROVIDERS:
                try:
                    extractor = Extractor(provider['name'], provider['url'])
                    extractor._getAllVideos()
                    for col in collections : self._util.exportCollection(col) 
                    self._util.setLastUpdated()
                except Exception as e:
                    print(e)



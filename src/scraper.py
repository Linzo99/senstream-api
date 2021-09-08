from mongoengine import connect
from .constants import PROVIDERS, collections
from .extractor import Extractor
from .util import Util
import asyncio


loop = asyncio.get_event_loop()
class Scraper:
    """ Class for scraping playlist videos """
    def __init__(self):
        self._util = Util()

    def scrape(self):
        for provider in PROVIDERS:
            try:
                extractor = Extractor(provider['name'], provider['url'])
                loop.run_until_complete(extractor._getAllVideos())
                for col in collections : self._util.exportCollection(col) 
            except Exception as e:
                print(e)


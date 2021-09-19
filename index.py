import time
from multiprocessing import Process

import uvicorn

from src.constants import dbName
from src.scraper import Scraper
from src.util import Util


class Index:
    _util = Util()
    _scraper = Scraper()
    def __init__(self, start=True, debug=False):
        Index._startAPI(start)

    @staticmethod
    def _startAPI(start):
        try:
            Index._util.setLastUpdated()
            if start : Process(target=Index._scraper.scrape).start()
            uvicorn.run('api:app', reload=True, debug=True, workers=3)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    Index._startAPI(False)

from src.scraper import Scraper
from src.util import Util
from src.constants import dbName
import schedule
from mongoengine import connect
import uvicorn

connect(dbName)

class Index:
    _util = Util()
    _scraper = Scraper()
    def __init__(self, start=True, debug=False):
        Index._startAPI(start)

    @staticmethod
    def _startAPI(start):
        try:
            #Index._util._createTemp() 
            Index._util.setLastUpdated()
            if start : Index._scraper.scrape()                
            print("API STARTED")
            uvicorn.run('api:app', reload=True, debug=True, workers=3)
            #schedule.every(10).hours.do(Index._scraper.scrape())
            #while True:
                #schedule.run_pending()
                #time.sleep(1)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    Index._startAPI(False)


    





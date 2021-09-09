import youtubesearchpython.__future__ as ytb
from .constants import VID_MAP
from .helper import Helper
import re

class Extractor:
    """ Class for extracting data from torrents """
    def __init__(self, name:str, provider:str):
        # The name of the playlist :type:str
        self.name = name
        # The url of the playlist :type:str
        self._provider = provider
        # initialise the helper
        self._helper = Helper(self.name)
        
    def _extractVideo(self, vid, title):
        """ Extract correctly the data for the model """
        title = title
        viewCount = int(vid['viewCount']['text']) if "viewCount" in vid else 0
        video = { key:vid.get(val, None) if key!="rating" else vid.get(val, 0) for key,val in VID_MAP.items() }
        video.update( { 'title':title, 'viewCount':viewCount })
        return self._helper.addVideo(video)



    def _getVideoData(self, vid:dict):
        """ Get movie information based on regex """
        one = re.compile(r'.*(sais\D*\d+).*(epis\D*\d+.*)', re.IGNORECASE)
        two = re.compile(r'.*(epis\D*\d+.*)', re.IGNORECASE)
        if one.match(vid['title']):
            title = self.name+" "+" - ".join(one.match(vid['title']).group(1, 2))
            return self._extractVideo(vid, title)
        elif two.match(vid['title']):
            title = self.name +' '+two.match(vid['title']).group(1)
            return self._extractVideo(vid, title)



    async def _getAllVideos(self):
        """ Get all videos on the playlist """
        try:
            playlist = ytb.Playlist(self._provider)
            print(self.name)
            while playlist.hasMoreVideos:
                print('Getting more videos ..............')
                await playlist.getNextVideos()
            print("Feched All videos !")

            for vid in playlist.videos:
                try:
                    data = await ytb.Video.getInfo(vid['link'])
                except:
                    data = vid
                channel = playlist.info['channel']['id']
                data.update( { 'duration': vid['duration'], 'playlist' : playlist.info, 'channel':channel} )
                video = self._getVideoData(data)
            return 

        except Exception as e:
            print("Error ", e)
from .models.Channel import Channel
from .models.Video import Video
import logging
from .models.Playlist import Playlist
from mongoengine import connect
from .constants import PLAY_MAP, CHAN_MAP
import re



class Helper:
    """ Helper for adding data in mongodb """
    def __init__(self, name:str):
        self.name = name
        connect("senstream")

    def _updateChannel(self, chan):
        """ Create a playlist or Update if exists """
        try:
            found = Channel.objects(pk=chan['id'])
            if found:
                found = found[0]
                # No update for the time being
            else:
                print(f"{chan['name']} is a new Channel")
                data = { key:chan[val] for key,val in CHAN_MAP.items() } 
                return Channel(**data).save()
        
        except Exception as e:
            print("Error Channel", e)

    def _parsePlaylist(self, play:dict):
        """ parse the Playlist """
        view_match = re.compile(r'(\d+).*')
        viewCount = view_match.match(play['viewCount']).group(1)
        videoCount = int(play['videoCount'])
        try:
            play['thumbnails'] = play['thumbnails']['thumbnails']
        except:
            play['thumbnails'] = play['thumbnails']
        data = { key:play[val] for key,val in PLAY_MAP.items() }
        data.update( {'title':self.name, 'viewCount' : int(viewCount), 'videoCount':videoCount, 'channel':play['channel']['id'] } )
        return data


    def _updatePlaylist(self, play):
        """ Create a playlist or Update if exists """
        found = Playlist.objects(pk=play['id'])
        if found :
            found = found[0]
            update = dict()
            if found.videoCount and found.videoCount < int(play['videoCount']):
                update.update(self._parsePlaylist(play))
            if found.viewCount and found.viewCount < update.get('viewCount', 0):
                update = update if update else self._parsePlaylist(play) 
        
            if len(update) :
                return found.update(**update)
        else:
            print(f"{play['title']} is a new Playlist")
            data = self._parsePlaylist(play)
            return Playlist(**data).save()

    def _updateVideo(self, vid):
        """ Add a video or Update if exist """
        try:
            found = Video.objects(pk=vid['_id'])
            if found :
                found = found[0]
                update = dict()
                print(f"{vid['title']} already exist")
                if found.viewCount and (found.viewCount < vid['viewCount']):
                    update['viewCount'] = vid['viewCount']
                if found.rating and (found.rating < vid['rating']):
                    update['rating'] = vid['rating']
                if found.title != vid['title']:
                    update['title'] = vid['title']
                if len(update) :
                    print(f"{vid['title']} is updating")
                    return found.update(**update)
            else:
                print(f"{vid['title']} is a new video")
                return Video(**vid).save()

        except Exception as e:
            print("Error Video", e)

    def addVideo(self, video:dict):
        """ update the video """
        return self._updateVideo(video)
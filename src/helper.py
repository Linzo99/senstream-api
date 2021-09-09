from .models.Channel import Channel
from .models.Video import Video
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
        play['thumbnails'] = play['thumbnails']['thumbnails']
        data = { key:play[val] for key,val in PLAY_MAP.items() }
        data.update( {'viewCount' : int(viewCount), 'videoCount':videoCount, 'channel':play['channel']['id'] } )
        return data


    def _updatePlaylist(self, play):
        """ Create a playlist or Update if exists """
        try:
            found = Playlist.objects(pk=play['id'])
            if found :
                found = found[0]
                update = dict()
                if found.videoCount and found.videoCount < int(play['videoCount']):
                    update.update(self._parsePlaylist(play))
                if found.viewCount and found.viewCount < update.get('viewCount', 0):
                    update = update if update else self._parsePlaylist(play) 
            
                if update :
                    return found.update(**update)
            else:
                print(f"{play['title']} is a new Playlist")
                self._updateChannel( play['channel'] )
                data = self._parsePlaylist(play)
                return Playlist(**data).save()

        except Exception as e:
            print("Error Playlist", e)


    def _updateVideo(self, vid):
        """ Add a video or Update if exist """
        try:
            found = Video.objects(pk=vid['_id'])
            if found :
                found = found[0]
                update = {'description':vid['description'], 'published':vid['published'], 'uploaded':vid['uploaded']}
                print(f"{vid['title']} already exist")
                if found.viewCount and found.viewCount < vid['viewCount']:
                    update['viewCount'] = vid['viewCount']
                elif found.rating and found.rating < vid['rating']:
                    update['rating'] = vid['rating']
                elif found.title != vid['title']:
                    print(f"{vid['title']} is updating")
                    update['title'] = vid['title']
                if update :
                    return found.update(**update)
            else:
                print(f"{vid['title']} is a new video")
                self._updatePlaylist( vid['playlist'] )
                vid['playlist'] = vid['playlist']['id']
                return Video(**vid).save()

        except Exception as e:
            print("Error Video", e)

    def addVideo(self, video:dict):
        """ update the video """
        return self._updateVideo(video)
import asyncio
import os

import click
import youtubesearchpython as ytb

from index import Index
from src.constants import collections, dbName
from src.extractor import Extractor
from src.models.Playlist import Playlist
from src.util import Util

util = Util() 
loop = asyncio.get_event_loop()


def handle_import(file):
    """" Handle the file import """
    try:
        parse = os.path.splitext(file)
        collection = os.path.basename(parse[0])
        util.importCollection(collection, file)
    except Exception as e:
        print(e)
        
def create_playlist(name:str, link:str):
    """ Add a new playlist or update if exists """
    extractor = Extractor(name, link)
    loop.run_until_complete(extractor._getAllVideos()) 
    for col in collections : util.exportCollection(col) 

def add_video(play_name:str, link:str):
    """ Add a new video or update if exists """
    extractor = Extractor(play_name, link)
    try:
        play = ytb.PlaylistsSearch(play_name, region="SN", limit=1)
        if play.result():
            _id = play.result()['result'][0]['id']
            exist = Playlist.objects(_id=_id)
            if exist:
                videoCount = play.result()['result'][0]['videoCount']
                play = {'id':_id, 'videoCount':videoCount }
                data = ytb.Video.getInfo(link)
                channel = data['channel']['id']
                data.update( {'playlist' : play, 'channel':channel} )
                video = extractor._getVideoData(data)
                for col in collections : util.exportCollection(col) 
            else:
                print("The video playlist is not in the database")
        else:
            print("No result found for the playlist")
    except Exception as e:
        print(e)



@click.command()
@click.option('-r', '--run', help="Run SenStream API and start scraping", is_flag=True)
@click.option('-s', '--server', help="Run SenStream API without scraping", is_flag=True)
@click.option('--scrape', help="Start Scraping", is_flag=True)
@click.option('-e', '--export', 'collection', help="Export a collection to a JSON file", type=str)
@click.option('-i', '--import', "file", help="Import a collection", type=click.Path(exists=True))
@click.option('-p', '--playlist', help="Add a new playlist", nargs=2, type=(str, str))
@click.option('-v', '--video', help="Add a new video <PlaylistName> <videoLink>", nargs=2, type=(str, str))
def cli(run, server, collection, file, playlist, video, scrape):
    if run :
        """ Run the API and start scraping """
        Index._startAPI(True) 
    elif server:
        """ Run the API without scraping """
        Index._startAPI(False) 
    elif scrape:
        """ Start the scraping process """
        Index._scraper.scrape()
    elif collection : 
        """ Export a collection """
        if collection in collections: util.exportCollection(collection)
        else: click.echo("This collection does not exist") 
    elif file : 
        """ import a file """
        test = click.confirm("Confirm the import ", default=False)
        if test : handle_import(file)
    elif playlist:
        test = click.confirm("Confirm the import ", default=False)
        if test:
            name, link = playlist
            create_playlist(name, link)
    elif video:
        test = click.confirm("Confirm the import ", default=False)
        if test:
            name, link = video
            add_video(name, link)

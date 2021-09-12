from typing import Dict, List
import os


""" List of sources to retrive Videos """
PROVIDERS : List[Dict[ str, str]] = [
    {
        'name': 'Impact',
        'url': 'https://www.youtube.com/playlist?list=PLg7NjHK9t-vtRERj-P5UXUN5MeYChZLlE'
    },
    {
        'name' : 'Yiddé',
        'url'  : 'https://www.youtube.com/playlist?list=PLg7NjHK9t-vvU8yWaHP95dn-VRLR95fG2'
    },
    {
        'name' : 'Arrêt Mère Thiaba',
        'url'  : 'https://www.youtube.com/playlist?list=PLg7NjHK9t-vum2WbRXVLS2zA8iGbTm1us'
    },
    {
        'name' : 'Les 4 Fantastique',
        'url'  : 'https://www.youtube.com/playlist?list=PLg7NjHK9t-vt3HjYkcgAtjH6WoRSwSafG'
    },
    {
        'name' : 'Virginie',
        'url'  : 'https://www.youtube.com/playlist?list=PLg7NjHK9t-vvLi7Q3ETCo6A_W5qXKqf8L'
    },
    {
        'name' : 'Infidèle',
        'url'  : 'https://www.youtube.com/playlist?list=PLPgAk0OTvFp8pwPvOyV3kScnORxTk3lRu'
    },
    {
        'name' : 'Karma',
        'url'  : 'https://www.youtube.com/playlist?list=PLg7NjHK9t-vtITsCtX129tT9P0k7h4tWi'
    },
    {
        'name' : "L'or de Ninki Nanka",
        'url'  : 'https://www.youtube.com/playlist?list=PLg7NjHK9t-vvUFX2Ln4J4zFSoY53smq4H'
    },
    {
        'name' : 'Yoon',
        'url'  : 'https://www.youtube.com/playlist?list=PLg7NjHK9t-vv7mbW2FrLoLY-U80HFTLtl'
    },
    {
        'name' : 'Boutikou Diogoye 2021',
        'url'  : 'https://www.youtube.com/playlist?list=PLg7NjHK9t-vtcLfyY2snGs9FidpU5JTe9'
    },
    {
        'name' : "Maitresse d'un Homme Marié",
        'url'  : 'https://www.youtube.com/playlist?list=PLg7NjHK9t-vt4YgmhZP6xBYq8psOyoz7n'
    }
]

""" Mapping the fields for the model """
VID_MAP : dict = {
    '_id' : 'id',
    'title': 'title',
    'thumbnails' : 'thumbnails',
    'description' : 'description',
    'rating' : 'averageRating',
    'viewCount' : 'viewCount',
    'published' : 'publishDate',
    'uploaded' : 'uploadDate',
    'duration' : 'duration',
    'playlist' : 'playlist',
    'channel' : 'channel',
    'keywords' : 'keywords',
    'link' : 'link'
}

""" Mapping playlist for the model """
PLAY_MAP : dict = {
    '_id' : 'id',
    'title' : 'title',
    'videoCount' : 'videoCount',
    'viewCount' : 'viewCount',
    'thumbnails' : 'thumbnails',
    'link' : 'link',
}

""" Mapping Channel for the model """
CHAN_MAP : dict = {
    '_id' : 'id',
    'name' : 'name',
    'thumbnails' : 'thumbnails',
    'link' : 'link',
}



dbName = "senstream"
tempDir = os.path.join(os.getcwd(), "tmp")
collections = ("videos", "channels", "playlists")
dbhost = "localhost"

# updated_file for recording the scrapping
updatedFile = "lastUpdated.txt"
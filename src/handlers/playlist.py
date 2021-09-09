import re
from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from ..models.Playlist import Playlist

router = APIRouter(prefix='/playlists')

class Thumb(BaseModel):
    url : str
    width : int
    height : int

class PlaylistModel(BaseModel):
    id : str
    title : str
    viewCount : int
    videoCount : int
    thumbnails : List[Thumb]
    link : str
    channel : str

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


@router.get('/', response_model=List[PlaylistModel])
def getAllPlaylist(ord:Optional[str]=None, sort:Optional[str]=None, c:Optional[str]=None, s:Optional[str]=None):
    """ Get all the playlists """
    if not sort: sort = ('-viewCount', '-videoCount')
    else: 
        if not ord : ord = "dec"
        if ord=="asc": sort = (sort,)
        if ord=="dec": sort = ('-'+sort,)

    playlists =  Playlist.objects.order_by(*sort)
    if c : playlists = playlists.filter(channel=c)
    if s : 
        regex = ""
        words = s.split('+')
        for w in words:
            regex += f".*({re.escape(w)}*).*"
        regex = re.compile(regex, flags=re.I | re.DOTALL)
        playlists = playlists.filter(title=regex)
    return list(playlists)


@router.get("/{id}", response_model=PlaylistModel)
def getPlaylist(id:str):
    """  Get playlist by id """
    try:
        playlist = Playlist.objects(_id=id).get()
        return playlist
    except Exception as e:
        return None

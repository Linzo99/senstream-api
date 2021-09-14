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

class ReturnData(BaseModel):
    results : List[PlaylistModel]
    page : int
    total_pages : int


@router.get('/', response_model=ReturnData)
def getAllPlaylist(ord:Optional[str]=None,
                   sort:Optional[str]=None,
                   page:Optional[int]=1,
                   c:Optional[str]=None, 
                   l:Optional[int]=15, 
                   s:Optional[str]=None):
    """ Get all the playlists 
        `sort` to sort by value (viewCount | rating | uploaded)
        `ord` for ordering the sorted result ( asc | desc )
        `c` to filter by channel
        `s` for searching
        `l` the number of result desired
    """
    offset = (page - 1) * l
    if not sort: sort = ('-viewCount', '-videoCount')
    else: 
        if not ord : ord = "dec"
        if ord=="asc": sort = (sort,)
        if ord=="dec": sort = ('-'+sort,)

    playlists =  Playlist.objects.order_by(*sort)[offset:offset+l]
    if c : playlists = playlists.filter(channel=c)
    if s : 
        regex = ""
        words = s.split('+')
        for w in words:
            regex += f".*({re.escape(w)}*).*"
        regex = re.compile(regex, flags=re.I | re.DOTALL)
        playlists = playlists.filter(title=regex)
    total_pages = round(playlists.count() / l)
    return {"results":list(playlists), "page":page, "total_pages":total_pages}


@router.get("/{id}", response_model=PlaylistModel)
def getPlaylist(id:str):
    """  Get playlist by id """
    try:
        playlist = Playlist.objects(_id=id).get()
        return playlist
    except Exception as e:
        return None

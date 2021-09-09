from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel
from ..models.Video import Video
import re

router = APIRouter(prefix='/videos')

class Thumb(BaseModel):
    url : str
    width : int
    height : int

class VideoModel(BaseModel):
    id : str
    title : str
    thumbnails : List[Thumb]
    viewCount : Optional[int] = None
    description : Optional[str] = None
    rating : Optional[float] = None
    published : Optional[str] = None
    uploaded : Optional[str] = None
    channel : Optional[str] = None
    keywords : List[str] = None
    duration : Optional[str] = None
    link : str
    playlist : str

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


@router.get('/', response_model=List[VideoModel])
def getAllVideos(ord:Optional[str]=None, sort:Optional[str]=None, c:Optional[str]=None, p:Optional[str]=None, s:Optional[str]=None):
    """ Get all the movies """
    if not sort: sort = ('-viewCount', '-rating')
    else: 
        if not ord : ord = "dec"
        if ord=="asc": sort = (sort,)
        if ord=="dec": sort = ('-'+sort,)

    videos =  Video.objects.order_by(*sort)
    if p : videos = videos.filter(playlist=p)
    elif c : videos = videos.filter(channel=c)
    if s : 
        regex = ""
        words = s.split('+')
        for w in words:
            regex += f".*({re.escape(w)}*).*"
        regex = re.compile(regex, flags=re.I | re.DOTALL)
        videos = videos.filter(title=regex)
    return list(videos)


@router.get("/{id}", response_model=VideoModel)
def getMovie(id:str):
    """  Get movie by id """
    try:
        movie = Video.objects(_id=id).get()
        return movie
    except Exception as e:
        return {}
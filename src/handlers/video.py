from typing import Optional, List, Dict
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

class ReturnData(BaseModel):
    results : List[VideoModel]
    page : int
    total_pages : int

@router.get('/', response_model=ReturnData)
def getAllVideos(ord:Optional[str]=None, 
                 sort:Optional[str]=None, 
                 page:Optional[int]=1, 
                 c:Optional[str]=None, 
                 p:Optional[str]=None, 
                 l:Optional[int]=15, 
                 s:Optional[str]=None):
    """ Get all the movies 
        `sort` to sort by value (viewCount | rating | uploaded)
        `ord` for ordering the sorted result ( asc | desc )
        `page` the desired page
        `c` to filter by channel
        `p` to filter by playlist
        `s` for searching
        `l` the number of result desired
    
    """
    offset = (page - 1) * l
    if not sort: sort = ('-viewCount', '-rating')
    else: 
        if not ord : ord = "dec"
        if ord=="asc": sort = (sort,)
        if ord=="dec": sort = ('-'+sort,)

    videos =  Video.objects.order_by(*sort)[offset:offset+l]
    if p : videos = videos.filter(playlist=p)
    elif c : videos = videos.filter(channel=c)
    if s : 
        regex = ""
        words = s.split('+')
        for w in words:
            regex += f".*({re.escape(w)}*).*"
        regex = re.compile(regex, flags=re.I | re.DOTALL)
        videos = videos.filter(title=regex)
    else: videos = videos.filter(title__not__icontains="annonce")
    total_pages = round(videos.count() / l)
    return { "results": list(videos), "page":page, "total_pages":total_pages}


@router.get("/{id}", response_model=VideoModel)
def getMovie(id:str):
    """  Get movie by id """
    try:
        movie = Video.objects(_id=id).get()
        return movie
    except Exception as e:
        return None
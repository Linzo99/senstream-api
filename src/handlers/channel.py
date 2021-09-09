from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel
from ..models.Channel import Channel


router = APIRouter(prefix="/channels")


class Thumb(BaseModel):
    url : str
    width : int
    height : int

class ChannelModel(BaseModel):
    id : str
    name : str
    thumbnails : List[Thumb]
    link : str

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


@router.get('/', response_model=List[ChannelModel])
def getAllChannels():
    """ Get all the channels """
    channels = Channel.objects.all()
    return list(channels)


@router.get('/{id}', response_model=ChannelModel)
def getChannel(id:str):
    """ Get channel by id """ 
    try:
        channel = Channel.objects(_id=id).get()
        return channel
    except Exception as e:
        return None


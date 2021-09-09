from mongoengine import connect
from fastapi import FastAPI
from src.handlers import video, channel, playlist
from src.constants import dbName

app = FastAPI()

""" routes for videos """
app.include_router(video.router)
""" routes for channels """
app.include_router(channel.router)
""" routes for playlists """
app.include_router(playlist.router)

@app.get("/")
def root():
    return {"Message": "Bienvenue dans SenStream"}

@app.on_event("startup")
def db_connection():
    """ Connect to db on start """
    app.db_client = connect(dbName)

@app.on_event("shutdown")
def db_connection():
    """ Connect to db on start """
    app.db_client.close()


from fastapi import FastAPI
from src.handlers import video, channel, playlist

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


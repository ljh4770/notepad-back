from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from router import user, note

from db import models
from db.database import engine

from auth import authentication

router = APIRouter()
@router.get('/api')
def index():
    return {"message": "Respond from notepad backend server"}

app = FastAPI()
app.include_router(authentication.router)
app.include_router(router)
app.include_router(user.router)
app.include_router(note.router)

origins = ["front_url"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

models.Base.metadata.create_all(engine)
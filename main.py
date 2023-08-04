from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, HTTPException
from starlette.middleware.cors import CORSMiddleware, HTTPException
from posts.router import router as posts_router 
from database import database
import requests
from typing import List

import cloudinary
from cloudinary.uploader import upload
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post('/images')
def upload_files(files: List[UploadFile]):
    urls = []
    for file in files:
        result = upload(file.file.read())
        urls.append(result['secure_url'])

    return {
        'urls': urls
    }


@app.post('/images')
def upload_files(files: List[UploadFile]):
    urls = []
    for file in files:
        result = upload(file.file.read())
        urls.append(result['secure_url'])

    return {
        'urls': urls
    }


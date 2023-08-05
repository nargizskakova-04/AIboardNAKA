from posts.schemas import CreatePostRequest, EditPostRequest, HaikuRequest, EditPostTextRequest
from fastapi import APIRouter, Depends, HTTPException
from posts import service
import os
import requests
from dotenv import load_dotenv

from sqlalchemy.orm import Session


from database import engine, database


load_dotenv()
token = os.environ.get("token")
MODEL_URL = "https://7583-185-48-148-173.ngrok-free.app/custom-prompt"
HEADERS = {"Authorization": f"Bearer {token}"}


router = APIRouter()


@router.get('')
async def get_posts():
    return await service.get_posts()

@router.post('')
async def create_post(post: CreatePostRequest):
    return await service.create_post(post)

@router.get('/{id}')
async def get_post(id: int):
    return await service.get_post_by_id(id)

@router.put('/{id}')
async def edit_post(id: int, post_data: EditPostRequest):
    return await service.edit_post(id, post_data)

@router.delete('/{id}')
async def delete_post(id: int):
    await service.delete_post(id)

    return {"message": "ok, deleted"}

@router.post('/generate-haiku')
async def generate_haiku(req: HaikuRequest):
    prompt_data = {
  "input_text": f"generate a traditional haiku with words {req.keywords}",
  "top_k": 40,
  "top_p": 0.95,
  "temp": 0.1,
  "repeat_penalty": 1.3,
  "repeat_last_n": 64,
  "n_predict": 128
}
    r = requests.post(url=MODEL_URL, json=prompt_data, headers=HEADERS).json()
    return r["output"]

async def get_post_text(id: int):
    select_query = f"SELECT text FROM posts WHERE id = {id}"
    post = await database.fetch_one(select_query)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    return post



#тут короч он тип текст вохвращает вродь как
def get_db():
    db = get_posts
    try:
        yield db 
    finally:
        db.close()

@router.put('/text/{id}')
async def edit_post_text(id: int, post_data: EditPostTextRequest, db: Session = Depends(get_db)):
    return await service.edit_post_text(db, id, post_data)
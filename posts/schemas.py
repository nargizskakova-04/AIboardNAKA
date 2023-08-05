from typing import Optional
from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    text: str
    author: str
    keywords: str


class EditPostRequest(BaseModel):
    keywords: Optional[str] = None
    text: Optional[str] = None
    author: Optional[str] = None

class EditPostTextRequest(BaseModel):
    text: Optional[str] = None

class HaikuRequest(BaseModel):
    keywords: str
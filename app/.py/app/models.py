from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserIn(BaseModel):
    name: str
    email: str

class UserOut(UserIn):
    id: str

class PostIn(BaseModel):
    user_id: str
    title: str
    body: str

class PostOut(PostIn):
    id: str
    created_at: datetime

class FileMeta(BaseModel):
    id: Optional[str]
    filename: str
    content_type: Optional[str] = None
    s3_key: str
    user_id: Optional[str] = None
    uploaded_at: Optional[datetime] = None

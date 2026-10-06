from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ArticleCreate(BaseModel):
    title: str
    text: str
    image: str
    category_id: int

class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    text: str
    image: str
    category_id: int
    created_at: datetime
    updated_at: datetime

class ArticleUpdate(BaseModel):
    title: str
    text: str
    image: str
    category_id: int

 
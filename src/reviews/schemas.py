import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field


class ReviewModel(BaseModel):
    id: uuid.UUID
    rating: int = Field(lt=5)
    review_text: str
    created_at: datetime
    updated_at: datetime
    user_id: Optional[uuid.UUID]
    book_id: Optional[uuid.UUID]


class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text: str

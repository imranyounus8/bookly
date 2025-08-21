import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from src.books.schemas import Book
from src.reviews.schemas import ReviewModel


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=12)
    last_name: str = Field(max_length=12)
    username: str = Field(max_length=8)
    email: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=12)
    phone_number: str = Field(max_length=12)


class UserModel(BaseModel):
    id: uuid.UUID
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password_hash: str = Field(exclude=True)
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=12)

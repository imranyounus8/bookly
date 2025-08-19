from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid
from typing import Optional
from src.auth import models


class BookModel(SQLModel, table=True):

    __tablename__ = "books"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    published_date: date
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now())
    )
    user_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.id"
    )
    user: Optional["models.User"] = Relationship(back_populates="users")

    def __repr__(self):
        return f"<Book {self.title}>"

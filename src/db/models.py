import uuid
from datetime import date, datetime
from typing import List, Optional

import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):

    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    role: str = Field(
        sa_column=Column(
            pg.VARCHAR, nullable=False, server_default="users"
        )
    )
    password_hash: str = Field(exclude=True)
    is_verified: bool = Field(
        sa_column=Column(pg.BOOLEAN, nullable=False, default=False)
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Book(SQLModel, table=True):

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
    user: Optional[User] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):

    __tablename__ = "reviews"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4
        )
    )
    rating: int = Field(lt=5)
    review_text: str
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now())
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now())
    )
    user_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.id"
    )
    book_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="books.id"
    )
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for Book {self.title} by user {self.user_id}.>"

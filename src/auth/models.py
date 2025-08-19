from sqlmodel import SQLModel, Field, Relationship
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column
from datetime import datetime
import uuid
from src.books import models
from typing import List


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
            pg.VARCHAR, nullable=False, server_default="user"
        )
    )
    password_hash: str = Field(exclude=True)
    is_verified: bool = Field(sa_column=Column(default=False))
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    books: List[models.BookModel] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"

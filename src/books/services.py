from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookCreateModel, BookUpdateModel
from .models import BookModel
from sqlmodel import select, desc
from datetime import datetime
import uuid


class BookService:
    async def get_books(self, session: AsyncSession):
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user_books(self, user_id: str, session: AsyncSession):
        statement = (
            select(BookModel)
            .where(BookModel.user_id == user_id)
            .order_by(desc(BookModel.created_at))
        )
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_id: str, session: AsyncSession):
        book_id = uuid.UUID(book_id)
        statement = select(BookModel).where(BookModel.id == book_id)
        result = await session.exec(statement)
        return result.first()

    async def create_book(
        self, book_data: BookCreateModel, user_id: str, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()
        new_book = BookModel(**book_data_dict)
        new_book.published_date = datetime.strptime(
            book_data.published_date, "%Y-%m-%d"
        )
        new_book.user_id = user_id
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(
        self, book_id: str, book_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_id, session)

        if book_to_update is not None:
            book_data_dict = book_data.model_dump()

            for k, v in book_data_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()
            return book_to_update

    async def delete_book(self, book_id: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_id, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()

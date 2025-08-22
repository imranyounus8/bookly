from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.services import BookService
from src.db.models import Tag
from src.tags.schemas import TagAddModel, TagCreateModel

book_service = BookService()


class TagService:
    async def get_tags(self, session: AsyncSession):
        statement = select(Tag).order_by(desc(Tag.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_tag(self, tag_id: str, session: AsyncSession):
        statement = select(Tag).where(Tag.id == tag_id)
        result = await session.exec(statement)
        return result.first()

    async def add_tags_to_book(
        self, book_id: str, tag_data: TagAddModel, session: AsyncSession
    ):
        book = await book_service.get_book(book_id=book_id, session=session)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Book not found."
            )
        for tag_item in tag_data.tags:
            result = await session.exec(
                select(Tag).where(Tag.name == tag_item.name)
            )
            tag = result.one_or_none()
            if not tag:
                tag = Tag(name=tag_item.name)
            book.tags.append(tag)

        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def add_tag(self, tag_data: TagCreateModel, session: AsyncSession):
        statement = select(Tag).where(Tag.name == tag_data.name)
        result = await session.exec(statement)
        tag = result.first()

        if tag:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tag already exists"
            )
        new_tag = Tag(name=tag_data.name)
        session.add(new_tag)
        await session.commit()
        return new_tag

    async def update_tag(
        self, tag_id: str, tag_data: TagCreateModel, session: AsyncSession
    ):
        tag = await self.get_tag(tag_id=tag_id, session=session)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        tag_dict = tag_data.model_dump()
        for k, v in tag_dict.items():
            setattr(tag, k, v)
            await session.commit()
            await session.refresh(tag)
        return tag

    async def delete_tag(self, tag_id: str, session: AsyncSession):
        tag = await self.get_tag(tag_id=tag_id, session=session)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        await session.delete(tag)
        await session.commit()
        return None

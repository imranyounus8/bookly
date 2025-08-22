from fastapi import APIRouter, Depends, status
from src.tags.services import TagService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.tags.schemas import TagModel, TagAddModel, TagCreateModel
from typing import List
from src.auth.dependencies import RoleChecker
from src.books.schemas import Book


tags_router = APIRouter()
tag_service = TagService()
role_checker = Depends(RoleChecker(['admin', 'user']))


@tags_router.get(
    '/',
    response_model=List[TagModel],
    dependencies=[role_checker]
)
async def retreive_tags(
    session: AsyncSession = Depends(get_session)
):
    tags = await tag_service.get_tags(session=session)
    return tags


@tags_router.post(
    '/',
    response_model=TagModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[role_checker]
)
async def add_tag(
    tag_data: TagCreateModel,
    session: AsyncSession = Depends(get_session)
) -> TagModel:
    added_tag = await tag_service.add_tag(
        tag_data=tag_data,
        session=session
    )
    return added_tag


@tags_router.post(
    '/book/{book_id}/tags',
    response_model=Book,
    dependencies=[role_checker]
)
async def add_tags_to_book(
    book_id: str,
    tag_data: TagAddModel,
    session: AsyncSession = Depends(get_session)
) -> Book:
    book_with_tag = await tag_service.add_tags_to_book(
        book_id=book_id,
        tag_data=tag_data,
        session=session
    )
    return book_with_tag


@tags_router.put(
    '/{tag_id}',
    response_model=TagModel,
    dependencies=[role_checker]
)
async def update_tag(
    tag_id: str,
    tag_update_data: TagCreateModel,
    session: AsyncSession = Depends(get_session)
) -> TagModel:
    updated_tag = await tag_service.update_tag(
        tag_id=tag_id,
        tag_data=tag_update_data,
        session=session
    )
    return updated_tag


@tags_router.delete(
    '/{tag_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker]
)
async def delete_tag(
    tag_id: str,
    session: AsyncSession = Depends(get_session)
):
    await tag_service.delete_tag(tag_id=tag_id, session=session)

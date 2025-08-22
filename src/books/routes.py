from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.books.schemas import (
    Book, BookCreateModel, BookUpdateModel, BookDetailsModel
)
from src.books.services import BookService
from src.db.main import get_session

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))


@book_router.get("/{book_id}", response_model=BookDetailsModel)
async def get_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    # print(user_details)
    book = await book_service.get_book(book_id, session)
    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found for the provided id",
        )


@book_router.get("/", response_model=List[Book])
async def get_books(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    books = await book_service.get_books(session)
    if books:
        return books
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No book found"
        )


@book_router.get(
    "/user/{user_id}",
    response_model=List[Book],
    dependencies=[role_checker]
)
async def get_user_book_submission(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    books = await book_service.get_user_books(user_id, session)
    if books:
        return books
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No book found"
        )


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[role_checker]
)
async def create_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    user_id = token_details.get('user')['user_id']
    new_book = await book_service.create_book(book_data, user_id, session)
    return new_book


@book_router.patch(
    "/{book_id}",
    response_model=Book,
    dependencies=[role_checker]
)
async def update_book(
    book_id: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    updated_book = await book_service.update_book(
        book_id, book_update_data, session
    )
    if updated_book:
        return updated_book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker]
)
async def delete_book(
    book_id: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    book_to_delete = await book_service.delete_book(book_id, session)
    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:
        return {}

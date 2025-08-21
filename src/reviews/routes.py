from fastapi import APIRouter, Depends
from src.reviews.services import ReviewService
from src.reviews.schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.db.models import User
from src.auth.dependencies import get_current_user

review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/book/{book_id}")
async def create_review(
    book_id: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await review_service.add_review_to_book(
        book_id=book_id,
        user_email=current_user.email,
        review_data=review_data,
        session=session
    )
    return new_review


@review_router.get('/')
async def retrieve_reviews(
    session: AsyncSession = Depends(get_session)
):
    reviews = await review_service.get_reviews(session)
    return reviews


@review_router.get('/{review_id}')
async def retrieve_review(
    review_id: str,
    session: AsyncSession = Depends(get_session)
):
    review = await review_service.get_review(review_id, session)
    return review


@review_router.delete('/{review_id}')
async def delete_a_review(
    review_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    await review_service.delete_review(
        review_id=review_id,
        user_email=current_user.email,
        session=session
    )
    return None

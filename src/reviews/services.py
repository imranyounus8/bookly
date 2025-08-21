from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.services import UserService
from src.books.services import BookService
from src.db.models import Review
from src.reviews.schemas import ReviewCreateModel
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel import select, desc

user_service = UserService()
book_service = BookService()


class ReviewService:
    async def add_review_to_book(
        self,
        book_id: str,
        user_email: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        try:
            user = await user_service.get_user_by_email(
                email=user_email, session=session
            )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )
            book = await book_service.get_book(book_id, session)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found."
                )
            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)
            new_review.user = user
            new_review.book = book
            session.add(new_review)
            await session.commit()
            return new_review

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Oops.... something went wrong. {e}",
            )

    async def get_review(self, review_id: str, session: AsyncSession):
        statement = select(Review).where(Review.id == review_id)
        result = await session.exec(statement)
        return result.first()

    async def get_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))
        result = await session.exec(statement)
        return result.all()

    async def delete_review(
        self, review_id: str, user_email: str, session: AsyncSession
    ):
        user = await user_service.get_user_by_email(user_email, session)
        print("User -->", user.id)
        review = await self.get_review(review_id, session)
        if not review or (review.user_id != user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete this review"
            )
        await session.delete(review)
        await session.commit()

from fastapi import APIRouter

tags_router = APIRouter()


@tags_router.post('/review/{review_id}')
async def tag_a_review():
    pass

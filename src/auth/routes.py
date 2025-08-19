from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from src.auth.services import UserService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.utils import create_access_token, verify_passwd
from datetime import timedelta, datetime
from src.auth.dependencies import (
    RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
)
from src.db.redis import add_jti_to_blocklist

auth_route = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin'])

REFRESH_TOKEN_EXPIRY = 2


@auth_route.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists with this email.",
        )
    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_route.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_passwd(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_id": str(user.id),
                    "role": user.role
                }
            )
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_id": str(user.id)},
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=True,
            )
            return JSONResponse(
                content={
                    "message": "Logged in succesfully.",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.id)},
                }
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or Password"
    )


@auth_route.get("/refresh")
async def refresh_token(
    token_details: dict = Depends(RefreshTokenBearer())
) -> dict:
    exp_timestamp = token_details['exp']
    if datetime.fromtimestamp(exp_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )
        return JSONResponse(
            content={
                "access_token": new_access_token
            }
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token."
    )


@auth_route.get('/me')
async def get_current_user(
    user: dict = Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_route.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti=jti)
    return JSONResponse(
        content={
            "message": "Logged out succesfully."
        },
        status_code=status.HTTP_200_OK
    )

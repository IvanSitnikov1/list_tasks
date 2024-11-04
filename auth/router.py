from fastapi import APIRouter, Form
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import SUserAdd, TokenInfo
from repository import UserRepository
from database import get_async_session


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/login', response_model=TokenInfo)
async def auth_user_issue_jwt(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(get_async_session),
):
    user_id = await UserRepository.get_user_id_for_auth(
        username, password, session)
    access_token = await UserRepository.create_access_token(user_id)
    refresh_token = await UserRepository.create_refresh_token(user_id)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )

@router.post('/register')
async def add_user(
        user_data: SUserAdd = Depends(),
        session: AsyncSession = Depends(get_async_session),
):
    await UserRepository.add_user(user_data, session)
    return {"status": "success"}

@router.post('/refresh', response_model=TokenInfo)
async def auth_refresh_jwt(refresh_token: str):
    user_id = await UserRepository.get_user_id_for_refresh(refresh_token)
    access_token = await UserRepository.create_access_token(user_id)
    refresh_token = await UserRepository.create_refresh_token(user_id)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )

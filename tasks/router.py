from typing import Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import SUser
from auth.utils import decode_jwt
from http_erors import token_error
from repository import TaskRepository, UserRepository
from database import get_async_session
from tasks.schemas import STaskAdd, STaskId, STask


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
    dependencies=[Depends(http_bearer)]
)

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session),
) -> SUser:
    try:
        payload = decode_jwt(token=token)
        if payload.get('token_type') != 'access':
            raise token_error
    except InvalidTokenError:
        raise token_error
    user_id = payload.get('sub')
    result = await UserRepository.get_user(user_id, session)
    if result:
        return result

@router.post('')
async def add_task(
        task_data: STaskAdd = Depends(),
        session: AsyncSession = Depends(get_async_session),
        user: SUser = Depends(get_current_user),
):
    await TaskRepository.add_task(task_data, session)
    return {"status": "success"}

@router.get('')
async def get_tasks(
        status: Optional[str] = None,
        session: AsyncSession = Depends(get_async_session),
        user: SUser = Depends(get_current_user),
) -> list[STask]:
    tasks = await TaskRepository.get_tasks(status, session)
    return tasks

@router.put('{task_id}')
async def update_task(
        task_id: int,
        updated_data: STaskAdd = Depends(),
        session: AsyncSession = Depends(get_async_session),
        user: SUser = Depends(get_current_user),
) -> STaskId:
    updated_task_id = await TaskRepository.update_task(
        task_id, updated_data, session)
    return {"id": updated_task_id}

@router.delete('{task_id}')
async def delete_task(
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: SUser = Depends(get_current_user),
) -> STaskId:
    await TaskRepository.delete_task(task_id, session)
    return {"id": task_id}

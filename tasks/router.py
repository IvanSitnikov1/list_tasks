from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from repository import TaskRepository
from database import get_async_session
from models import task
from tasks.schemas import STaskAdd, STaskId, STask

router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
)

@router.post('')
async def add_task(
        task_data: STaskAdd = Depends(),
        session: AsyncSession = Depends(get_async_session),
):
    await TaskRepository.add_task(task_data, session)
    return {"status": "success"}

@router.get('')
async def get_tasks(
        status: Optional[str] = None,
        session: AsyncSession = Depends(get_async_session),
) -> list[STask]:
    tasks = await TaskRepository.get_tasks(status, session)
    return tasks

@router.put('{task_id}')
async def update_task(
        task_id: int,
        updated_data: STaskAdd = Depends(),
        session: AsyncSession = Depends(get_async_session),
) -> STaskId:
    updated_task_id = await TaskRepository.update_task(
        task_id, updated_data, session)
    return {"id": updated_task_id}

@router.delete('{task_id}')
async def delete_task(
        task_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> STaskId:
    await TaskRepository.delete_task(task_id, session)
    return {"id": task_id}

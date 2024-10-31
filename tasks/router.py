from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends

from repository import TaskRepository
from tasks.schemas import STaskAdd, STaskId, STask

router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
)

@router.post('')
async def add_task(task: STaskAdd = Depends()) -> STaskId:
    new_task_id = await TaskRepository.add_task(task)
    return {"id": new_task_id}

@router.get('')
async def get_tasks(status: Optional[str] = None) -> list[STask]:
    tasks = await TaskRepository.get_tasks(status)
    return tasks

@router.put('{task_id}')
async def update_task(task_id: int, updated_data: STaskAdd = Depends()) -> STaskId:
    updated_task_id = await TaskRepository.update_task(task_id, updated_data)
    return {"id": updated_task_id}

@router.delete('{task_id}')
async def delete_task(task_id: int) -> STaskId:
    await TaskRepository.delete_task(task_id)
    return {"id": task_id}

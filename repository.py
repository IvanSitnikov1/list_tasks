from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, update, delete

from database import TaskOrm, new_session
from tasks.schemas import STaskAdd, STask


class TaskRepository:
    @classmethod
    async def add_task(cls, task: STaskAdd) -> int:
        async with new_session() as session:
            data = task.model_dump()
            new_task = TaskOrm(**data)
            session.add(new_task)
            await session.flush()
            await session.commit()
            return new_task.id

    @classmethod
    async def get_tasks(cls, status: Optional[str] = None) -> list[STask]:
        async with new_session() as session:
            if status:
                query = select(TaskOrm).where(TaskOrm.status == status)
            else:
                query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks = [STask.model_validate(task_model) for task_model in task_models]
            return tasks

    @classmethod
    async def update_task(cls, task_id: int, updated_data: STaskAdd) -> int:
        async with new_session() as session:
            updated_data = updated_data.model_dump()
            stmt = update(TaskOrm).where(TaskOrm.id == task_id).values(
                **updated_data
            )
            result = await session.execute(stmt)
            if not result.rowcount:
                raise HTTPException(status_code=404, detail="Task not found")
            await session.commit()
            return task_id

    @classmethod
    async def delete_task(cls, task_id: int) -> int:
        async with new_session() as session:
            stmt = delete(TaskOrm).where(TaskOrm.id == task_id)
            result = await session.execute(stmt)
            if not result.rowcount:
                raise HTTPException(status_code=404, detail="Task not found")
            await session.commit()
            return task_id

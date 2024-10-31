from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession


from models import task
from tasks.schemas import STaskAdd, STask


class TaskRepository:
    @classmethod
    async def add_task(cls, task_data: STaskAdd, session: AsyncSession):
        data = task_data.model_dump()
        stmt = insert(task).values(**data)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def get_tasks(
            cls,
            status: Optional[str],
            session: AsyncSession,
    ) -> list[STask]:
        if status:
            query = select(task).where(task.c.status == status)
        else:
            query = select(task)
        result = await session.execute(query)
        dict_tasks = result.mappings().all()
        tasks = [STask(**el) for el in dict_tasks]
        return tasks

    @classmethod
    async def update_task(
            cls,
            task_id: int,
            updated_data: STaskAdd,
            session: AsyncSession,
    ) -> int:
        updated_data = updated_data.model_dump()
        stmt = update(task).where(task.c.id == task_id).values(
            **updated_data
        )
        result = await session.execute(stmt)
        if not result.rowcount:
            raise HTTPException(status_code=404, detail="Task not found")
        await session.commit()
        return task_id

    @classmethod
    async def delete_task(cls, task_id: int, session: AsyncSession) -> int:
        stmt = delete(task).where(task.c.id == task_id)
        result = await session.execute(stmt)
        if not result.rowcount:
            raise HTTPException(status_code=404, detail="Task not found")
        await session.commit()
        return task_id

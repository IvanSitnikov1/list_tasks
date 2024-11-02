import ast
from typing import Optional

from fastapi import HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import SUserAdd, SUser
from config import EXPIRE_MINUTES_ACCESS, EXPIRE_MINUTES_REFRESH
from models import task, user
from tasks.schemas import STaskAdd, STask
from auth.utils import hash_password, validate_password, create_jwt, decode_jwt


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


class UserRepository:
    @classmethod
    async def add_user(cls, user_data: SUserAdd, session: AsyncSession):
        data = user_data.model_dump()
        stmt = insert(user).values(username=data['username'],
                                   password_hash=str(hash_password(data['password'])))
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def get_user(cls, user_id, session: AsyncSession):
        query = select(user).where(user.c.id == user_id)
        result = await session.execute(query)
        user_obj = result.first()
        if user_obj:
            return SUser(id=user_obj[0], username=user_obj[1], password_hash=user_obj[2])

    @classmethod
    async def get_user_id_for_refresh(cls, refresh_token):
        token_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
        )
        try:
            payload = decode_jwt(refresh_token)
            if payload.get('token_type') != 'refresh':
                raise token_error
        except InvalidTokenError:
            raise token_error
        return payload.get('sub')

    @classmethod
    async def get_user_id_for_auth(
            cls,
            username: str,
            password: str,
            session: AsyncSession
    ):
        query = select(user).where(user.c.username == username)
        result = await session.execute(query)
        user_obj = result.first()
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid username or password',
        )
        if user_obj:
            if validate_password(password, ast.literal_eval(user_obj[2])):
                user_id = user_obj[0]
                return user_id
        raise unauthed_exc

    @classmethod
    async def create_access_token(cls, user_id: int):
        jwt_payload = {"sub": user_id}
        access_token = create_jwt(
            token_type='access',
            token_data=jwt_payload,
            expire_minutes=EXPIRE_MINUTES_ACCESS,
        )
        return access_token

    @classmethod
    async def create_refresh_token(cls, user_id: int):
        jwt_payload = {"sub": user_id}
        refresh_token = create_jwt(
            token_type='refresh',
            token_data=jwt_payload,
            expire_minutes=EXPIRE_MINUTES_REFRESH,
        )
        return refresh_token

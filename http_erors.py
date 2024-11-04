from fastapi import HTTPException, status


token_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token',
    )

task_not_found = HTTPException(status_code=404, detail="Task not found")

unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='invalid username or password',
)

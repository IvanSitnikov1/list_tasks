from sqlalchemy import Table, Column, Integer, String

from database import metadata


task = Table(
    "task",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("description", String(250), nullable=True),
    Column("status", String(30), nullable=False),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(100), nullable=False),
    Column("password_hash", String(1024), nullable=False)
)
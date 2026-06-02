from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, auth

async def get_user_by_username(db: AsyncSession, username: str):
    q = select(models.User).where(models.User.username == username)
    res = await db.execute(q)
    return res.scalars().first()

async def create_user(db: AsyncSession, username: str, password: str):
    hashed = auth.get_password_hash(password)
    user = models.User(username=username, hashed_password=hashed)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def create_task(db: AsyncSession, owner: models.User, title: str, description: str | None):
    task = models.Task(title=title, description=description, owner=owner)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def list_tasks(db: AsyncSession, owner_id: int):
    q = select(models.Task).where(models.Task.owner_id == owner_id).order_by(models.Task.created_at.desc())
    res = await db.execute(q)
    return res.scalars().all()

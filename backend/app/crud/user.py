from typing import Optional
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        id=str(uuid4()),
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        name=user_in.name,
        training_level=user_in.training_level,
        visibility=user_in.visibility
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user: User, user_in: UserUpdate) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    await db.flush()
    await db.refresh(user)
    return user


async def create_oauth_user(
    db: AsyncSession,
    email: str,
    name: str,
    provider: str,
    oauth_id: str,
    photo_url: Optional[str] = None
) -> User:
    user = User(
        id=str(uuid4()),
        email=email,
        name=name,
        oauth_provider=provider,
        oauth_id=oauth_id,
        photo_url=photo_url,
        is_verified=True
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

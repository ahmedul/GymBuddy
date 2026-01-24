from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import NotificationToken
from app.schemas.notification import NotificationTokenCreate


async def get_user_tokens(db: AsyncSession, user_id: str) -> List[NotificationToken]:
    """Get all active notification tokens for a user."""
    result = await db.execute(
        select(NotificationToken)
        .where(NotificationToken.user_id == user_id)
        .where(NotificationToken.is_active.is_(True))
    )
    return list(result.scalars().all())


async def get_token_by_value(db: AsyncSession, token: str) -> Optional[NotificationToken]:
    """Get a notification token by its value."""
    result = await db.execute(
        select(NotificationToken).where(NotificationToken.token == token)
    )
    return result.scalar_one_or_none()


async def register_token(
    db: AsyncSession,
    user_id: str,
    token_in: NotificationTokenCreate
) -> NotificationToken:
    """Register a new notification token or update existing one."""
    # Check if token already exists
    existing = await get_token_by_value(db, token_in.token)
    
    if existing:
        # Update to new user if token already exists
        existing.user_id = user_id
        existing.device_type = token_in.device_type
        existing.is_active = True
        existing.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(existing)
        return existing
    
    # Create new token
    token = NotificationToken(
        id=str(uuid4()),
        user_id=user_id,
        token=token_in.token,
        device_type=token_in.device_type,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(token)
    await db.commit()
    await db.refresh(token)
    return token


async def unregister_token(db: AsyncSession, token: str) -> bool:
    """Unregister (delete) a notification token."""
    result = await db.execute(
        delete(NotificationToken).where(NotificationToken.token == token)
    )
    await db.commit()
    return result.rowcount > 0


async def deactivate_token(db: AsyncSession, token: str) -> bool:
    """Mark a token as inactive (for failed deliveries)."""
    existing = await get_token_by_value(db, token)
    if existing:
        existing.is_active = False
        existing.updated_at = datetime.utcnow()
        await db.commit()
        return True
    return False


async def get_tokens_for_users(
    db: AsyncSession,
    user_ids: List[str]
) -> List[NotificationToken]:
    """Get all active tokens for multiple users."""
    result = await db.execute(
        select(NotificationToken)
        .where(NotificationToken.user_id.in_(user_ids))
        .where(NotificationToken.is_active.is_(True))
    )
    return list(result.scalars().all())

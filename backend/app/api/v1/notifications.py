from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user
from app.crud.notification import (
    register_token,
    unregister_token,
    get_user_tokens
)
from app.schemas.notification import (
    NotificationTokenCreate,
    NotificationTokenResponse,
    NotificationPreferences,
    NotificationPreferencesUpdate
)
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/token", response_model=NotificationTokenResponse, status_code=status.HTTP_201_CREATED)
async def register_push_token(
    token_in: NotificationTokenCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Register a push notification token for the current user."""
    token = await register_token(db, current_user.id, token_in)
    return token


@router.delete("/token")
async def unregister_push_token(
    token_in: NotificationTokenCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Unregister a push notification token."""
    deleted = await unregister_token(db, token_in.token)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found"
        )
    return {"status": "deleted"}


@router.get("/tokens", response_model=List[NotificationTokenResponse])
async def list_my_tokens(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all registered tokens for the current user."""
    tokens = await get_user_tokens(db, current_user.id)
    return tokens


@router.get("/preferences", response_model=NotificationPreferences)
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
):
    """Get notification preferences for the current user."""
    return NotificationPreferences(
        notify_session_invites=getattr(current_user, 'notify_session_invites', True),
        notify_friend_requests=getattr(current_user, 'notify_friend_requests', True),
        notify_session_reminders=getattr(current_user, 'notify_session_reminders', True)
    )


@router.patch("/preferences", response_model=NotificationPreferences)
async def update_notification_preferences(
    prefs: NotificationPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update notification preferences for the current user."""
    if prefs.notify_session_invites is not None:
        current_user.notify_session_invites = prefs.notify_session_invites
    if prefs.notify_friend_requests is not None:
        current_user.notify_friend_requests = prefs.notify_friend_requests
    if prefs.notify_session_reminders is not None:
        current_user.notify_session_reminders = prefs.notify_session_reminders
    
    await db.commit()
    await db.refresh(current_user)
    
    return NotificationPreferences(
        notify_session_invites=current_user.notify_session_invites,
        notify_friend_requests=current_user.notify_friend_requests,
        notify_session_reminders=current_user.notify_session_reminders
    )

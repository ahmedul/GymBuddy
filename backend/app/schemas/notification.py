from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NotificationTokenCreate(BaseModel):
    token: str = Field(..., min_length=10, max_length=500)
    device_type: Optional[str] = Field(None, pattern="^(ios|android|web)$")


class NotificationTokenResponse(BaseModel):
    id: str
    token: str
    device_type: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class NotificationPreferences(BaseModel):
    notify_session_invites: bool = True
    notify_friend_requests: bool = True
    notify_session_reminders: bool = True


class NotificationPreferencesUpdate(BaseModel):
    notify_session_invites: Optional[bool] = None
    notify_friend_requests: Optional[bool] = None
    notify_session_reminders: Optional[bool] = None

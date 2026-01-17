from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.social import FriendshipStatus, GroupRole
from app.schemas.user import UserPublicResponse


class FriendRequest(BaseModel):
    addressee_id: str


class FriendshipResponse(BaseModel):
    id: str
    requester_id: str
    addressee_id: str
    status: FriendshipStatus
    created_at: datetime

    class Config:
        from_attributes = True


class FriendResponse(BaseModel):
    user: UserPublicResponse
    friendship_id: str
    since: datetime


class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_private: bool = True
    max_members: int = 50


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    is_private: Optional[bool] = None


class GroupResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    photo_url: Optional[str] = None
    owner_id: str
    is_private: bool
    max_members: int
    created_at: datetime

    class Config:
        from_attributes = True


class GroupMemberResponse(BaseModel):
    user: UserPublicResponse
    role: GroupRole
    joined_at: datetime

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.models.user import TrainingLevel, ProfileVisibility


class UserBase(BaseModel):
    email: EmailStr
    name: str
    training_level: TrainingLevel = TrainingLevel.BEGINNER
    visibility: ProfileVisibility = ProfileVisibility.PRIVATE


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    photo_url: Optional[str] = None
    bio: Optional[str] = None
    training_level: Optional[TrainingLevel] = None
    visibility: Optional[ProfileVisibility] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    photo_url: Optional[str] = None
    bio: Optional[str] = None
    training_level: TrainingLevel
    visibility: ProfileVisibility
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserPublicResponse(BaseModel):
    id: str
    name: str
    photo_url: Optional[str] = None
    bio: Optional[str] = None
    training_level: TrainingLevel

    class Config:
        from_attributes = True

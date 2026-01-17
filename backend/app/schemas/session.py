from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.session import SessionVisibility, RSVPStatus
from app.schemas.user import UserPublicResponse
from app.schemas.gym import GymResponse


class ExerciseBase(BaseModel):
    name: str
    sets: Optional[int] = None
    reps: Optional[str] = None
    duration_seconds: Optional[int] = None
    notes: Optional[str] = None
    order: int = 0


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseResponse(ExerciseBase):
    id: str

    class Config:
        from_attributes = True


class SessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_at: datetime
    duration_minutes: int = 60
    visibility: SessionVisibility = SessionVisibility.FRIENDS
    max_participants: Optional[int] = None


class SessionCreate(SessionBase):
    gym_id: str
    group_id: Optional[str] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None
    exercises: List[ExerciseCreate] = []


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    visibility: Optional[SessionVisibility] = None
    max_participants: Optional[int] = None
    is_cancelled: Optional[bool] = None


class SessionParticipantResponse(BaseModel):
    id: str
    user: UserPublicResponse
    rsvp_status: RSVPStatus
    checked_in: bool
    checked_in_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SessionResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    gym: GymResponse
    scheduled_at: datetime
    duration_minutes: int
    visibility: SessionVisibility
    max_participants: Optional[int] = None
    creator: UserPublicResponse
    is_recurring: bool
    is_cancelled: bool
    participant_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class SessionDetailResponse(SessionResponse):
    participants: List[SessionParticipantResponse] = []
    exercises: List[ExerciseResponse] = []
    group_id: Optional[str] = None


class SessionInvite(BaseModel):
    user_ids: List[str]
    message: Optional[str] = None
    exercise_ids: Optional[List[str]] = None  # For targeted exercise invites


class RSVPRequest(BaseModel):
    status: RSVPStatus


class SessionFeedQuery(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: float = 10.0
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    include_public: bool = True

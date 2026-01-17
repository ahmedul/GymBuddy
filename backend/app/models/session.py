from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.gym import Gym


class SessionVisibility(str, enum.Enum):
    PRIVATE = "private"      # Only invited
    FRIENDS = "friends"      # Friends can see
    GROUP = "group"          # Group members only
    PUBLIC = "public"        # Anyone nearby


class RSVPStatus(str, enum.Enum):
    GOING = "going"
    MAYBE = "maybe"
    NOT_GOING = "not_going"


class Session(Base):
    __tablename__ = "sessions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Location
    gym_id: Mapped[str] = mapped_column(String(36), ForeignKey("gyms.id"))
    
    # Schedule
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    
    # Visibility & Access
    visibility: Mapped[SessionVisibility] = mapped_column(
        SQLEnum(SessionVisibility), default=SessionVisibility.FRIENDS
    )
    group_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("groups.id"), nullable=True
    )
    max_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Creator
    creator_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    
    # Recurring
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    recurrence_rule: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Status
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    creator: Mapped["User"] = relationship(back_populates="sessions_created")
    gym: Mapped["Gym"] = relationship(back_populates="sessions")
    group: Mapped[Optional["Group"]] = relationship(back_populates="sessions")
    participants: Mapped[List["SessionParticipant"]] = relationship(back_populates="session")
    exercises: Mapped[List["SessionExercise"]] = relationship(back_populates="session")


class SessionParticipant(Base):
    __tablename__ = "session_participants"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("sessions.id"))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    
    rsvp_status: Mapped[RSVPStatus] = mapped_column(
        SQLEnum(RSVPStatus), default=RSVPStatus.GOING
    )
    
    # Check-in
    checked_in: Mapped[bool] = mapped_column(Boolean, default=False)
    checked_in_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Invite info
    invited_by_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    invite_message: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session: Mapped["Session"] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship(back_populates="session_participations")


class SessionExercise(Base):
    __tablename__ = "session_exercises"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("sessions.id"))
    
    name: Mapped[str] = mapped_column(String(100))
    sets: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reps: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., "8-12"
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session: Mapped["Session"] = relationship(back_populates="exercises")


# Imports at end to avoid circular imports - required by SQLAlchemy
from app.models.user import User  # noqa: E402
from app.models.gym import Gym  # noqa: E402
from app.models.social import Group  # noqa: E402

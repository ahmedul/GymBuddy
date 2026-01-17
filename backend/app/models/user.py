from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.session import Base


class TrainingLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ProfileVisibility(str, enum.Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    PRIVATE = "private"


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Profile
    name: Mapped[str] = mapped_column(String(100))
    photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    training_level: Mapped[TrainingLevel] = mapped_column(
        SQLEnum(TrainingLevel), default=TrainingLevel.BEGINNER
    )
    
    # Privacy
    visibility: Mapped[ProfileVisibility] = mapped_column(
        SQLEnum(ProfileVisibility), default=ProfileVisibility.PRIVATE
    )
    
    # OAuth
    oauth_provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    oauth_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    favorite_gyms: Mapped[List["UserFavoriteGym"]] = relationship(back_populates="user")
    sessions_created: Mapped[List["Session"]] = relationship(back_populates="creator")
    session_participations: Mapped[List["SessionParticipant"]] = relationship(back_populates="user")


class UserFavoriteGym(Base):
    __tablename__ = "user_favorite_gyms"
    
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    gym_id: Mapped[str] = mapped_column(String(36), ForeignKey("gyms.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    user: Mapped["User"] = relationship(back_populates="favorite_gyms")
    gym: Mapped["Gym"] = relationship(back_populates="favorited_by")

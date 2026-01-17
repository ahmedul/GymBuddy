from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.user import UserFavoriteGym


class Gym(Base):
    __tablename__ = "gyms"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    address: Mapped[str] = mapped_column(String(500))
    
    # Geo coordinates
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    
    # Optional details
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # External IDs (for deduplication)
    google_place_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, unique=True)
    
    # Custom location flag (user-created)
    is_custom: Mapped[bool] = mapped_column(default=False)
    created_by_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=True
    )
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    favorited_by: Mapped[List["UserFavoriteGym"]] = relationship(back_populates="gym")
    sessions: Mapped[List["Session"]] = relationship(back_populates="gym")


# Import at end to avoid circular imports - required by SQLAlchemy
from app.models.user import UserFavoriteGym  # noqa: E402
from app.models.session import Session  # noqa: E402

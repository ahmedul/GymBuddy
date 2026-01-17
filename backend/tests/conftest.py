"""
Pytest configuration and fixtures for GymBuddy tests.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from uuid import uuid4
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.user import User, TrainingLevel, ProfileVisibility
from app.models.gym import Gym
from app.models.session import Session, SessionVisibility, SessionExercise
from app.models.social import Friendship, FriendshipStatus, Group
from app.core.security import create_access_token


# ============== User Fixtures ==============

@pytest.fixture
def mock_user() -> User:
    """Create a mock user for testing."""
    user = MagicMock(spec=User)
    user.id = str(uuid4())
    user.email = "test@example.com"
    user.name = "Test User"
    user.hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYLGpOBdvNem"  # Pre-hashed password
    user.photo_url = None
    user.bio = "Test bio"
    user.training_level = TrainingLevel.BEGINNER
    user.visibility = ProfileVisibility.PRIVATE
    user.is_active = True
    user.is_verified = False
    user.created_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()
    return user


@pytest.fixture
def mock_user_2() -> User:
    """Create a second mock user for friend/social tests."""
    user = MagicMock(spec=User)
    user.id = str(uuid4())
    user.email = "friend@example.com"
    user.name = "Friend User"
    user.hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYLGpOBdvNem"  # Pre-hashed password
    user.photo_url = None
    user.bio = "Friend bio"
    user.training_level = TrainingLevel.INTERMEDIATE
    user.visibility = ProfileVisibility.FRIENDS
    user.is_active = True
    user.is_verified = True
    user.created_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()
    return user


@pytest.fixture
def auth_token(mock_user) -> str:
    """Create a valid JWT token for the mock user."""
    return create_access_token(data={"sub": mock_user.id})


@pytest.fixture
def auth_headers(auth_token) -> dict:
    """Create authorization headers with bearer token."""
    return {"Authorization": f"Bearer {auth_token}"}


# ============== Gym Fixtures ==============

@pytest.fixture
def mock_gym() -> Gym:
    """Create a mock gym for testing."""
    gym = MagicMock(spec=Gym)
    gym.id = str(uuid4())
    gym.name = "Iron Paradise"
    gym.address = "123 Fitness St, New York, NY"
    gym.latitude = 40.7128
    gym.longitude = -74.0060
    gym.is_custom = False
    gym.phone = "+1-555-123-4567"
    gym.website = "https://ironparadise.example.com"
    gym.created_by_id = None
    gym.created_at = datetime.utcnow()
    return gym


# ============== Session Fixtures ==============

@pytest.fixture
def mock_session(mock_user, mock_gym) -> Session:
    """Create a mock session for testing."""
    session = MagicMock(spec=Session)
    session.id = str(uuid4())
    session.title = "Morning Strength Training"
    session.description = "Upper body focus"
    session.gym_id = mock_gym.id
    session.gym = mock_gym
    session.creator_id = mock_user.id
    session.creator = mock_user
    session.scheduled_at = datetime(2026, 1, 20, 7, 0, 0)
    session.duration_minutes = 90
    session.visibility = SessionVisibility.PUBLIC
    session.max_participants = 6
    session.is_recurring = False
    session.is_cancelled = False
    session.participants = []
    session.exercises = []
    session.created_at = datetime.utcnow()
    return session


@pytest.fixture
def mock_exercise() -> SessionExercise:
    """Create a mock exercise for testing."""
    exercise = MagicMock(spec=SessionExercise)
    exercise.id = str(uuid4())
    exercise.name = "Bench Press"
    exercise.sets = 4
    exercise.reps = "8-10"
    exercise.duration_seconds = None
    exercise.notes = "Focus on form"
    exercise.order = 1
    return exercise


# ============== Social Fixtures ==============

@pytest.fixture
def mock_friendship(mock_user, mock_user_2) -> Friendship:
    """Create a mock friendship for testing."""
    friendship = MagicMock(spec=Friendship)
    friendship.id = str(uuid4())
    friendship.requester_id = mock_user.id
    friendship.addressee_id = mock_user_2.id
    friendship.status = FriendshipStatus.PENDING
    friendship.created_at = datetime.utcnow()
    friendship.updated_at = datetime.utcnow()
    return friendship


@pytest.fixture
def mock_group(mock_user) -> Group:
    """Create a mock group for testing."""
    group = MagicMock(spec=Group)
    group.id = str(uuid4())
    group.name = "Morning Lifters"
    group.description = "Early birds who lift heavy"
    group.owner_id = mock_user.id
    group.owner = mock_user
    group.is_public = True
    group.created_at = datetime.utcnow()
    return group


# ============== Database Mock Fixtures ==============

@pytest.fixture
def mock_db():
    """Create a mock database session."""
    db = AsyncMock()
    db.execute = AsyncMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    db.add = MagicMock()
    return db


# ============== Client Fixtures ==============

@pytest.fixture
async def async_client():
    """Create an async HTTP client for API testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

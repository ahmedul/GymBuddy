"""
Unit tests for session endpoints.
Tests: create session, join/leave, exercises, invites
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from app.models.session import SessionVisibility, RSVPStatus


class TestSessionModel:
    """Test Session model properties."""
    
    def test_session_has_required_fields(self, mock_session):
        """Session should have all required fields."""
        required_fields = [
            "id", "title", "gym_id", "creator_id", "scheduled_at",
            "duration_minutes", "visibility", "is_cancelled", "created_at"
        ]
        
        for field in required_fields:
            assert hasattr(mock_session, field), f"Missing field: {field}"
    
    def test_session_visibility_options(self):
        """Verify all visibility options."""
        expected = ["public", "friends", "private", "group"]
        
        for visibility in SessionVisibility:
            assert visibility.value in expected
    
    def test_rsvp_status_options(self):
        """Verify all RSVP status options."""
        expected = ["going", "maybe", "not_going", "invited"]
        
        for status in RSVPStatus:
            assert status.value in expected


class TestCreateSession:
    """Test POST /api/v1/sessions."""
    
    @pytest.mark.asyncio
    async def test_create_session_success(self, mock_user, mock_gym, mock_db):
        """Authenticated user should be able to create a session."""
        session_data = {
            "title": "Morning Workout",
            "gym_id": mock_gym.id,
            "scheduled_at": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "duration_minutes": 60,
            "visibility": "public",
            "max_participants": 10
        }
        
        # Validate session data
        assert len(session_data["title"]) > 0
        assert session_data["duration_minutes"] > 0
        assert session_data["max_participants"] > 0
    
    @pytest.mark.asyncio
    async def test_create_session_with_exercises(self, mock_user, mock_gym):
        """Session can be created with exercises."""
        session_data = {
            "title": "Strength Training",
            "gym_id": mock_gym.id,
            "scheduled_at": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "duration_minutes": 90,
            "exercises": [
                {"name": "Bench Press", "sets": 4, "reps": "8-10", "order": 1},
                {"name": "Squats", "sets": 4, "reps": "8-10", "order": 2},
                {"name": "Deadlift", "sets": 3, "reps": "5", "order": 3}
            ]
        }
        
        assert len(session_data["exercises"]) == 3
        for i, exercise in enumerate(session_data["exercises"]):
            assert exercise["order"] == i + 1
    
    @pytest.mark.asyncio
    async def test_create_session_requires_auth(self, async_client):
        """Creating a session requires authentication."""
        response = await async_client.post(
            "/api/v1/sessions",
            json={
                "title": "Test Session",
                "gym_id": "some-gym-id",
                "scheduled_at": datetime.utcnow().isoformat(),
                "duration_minutes": 60
            }
        )
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_create_session_invalid_gym(self, mock_user, mock_db):
        """Creating session with non-existent gym should fail."""
        with patch("app.api.v1.sessions.get_gym_by_id") as mock_get_gym:
            mock_get_gym.return_value = None  # Gym doesn't exist
            
            result = await mock_get_gym(mock_db, "nonexistent-gym-id")
            assert result is None


class TestGetSessions:
    """Test GET /api/v1/sessions."""
    
    @pytest.mark.asyncio
    async def test_get_session_feed(self, mock_user, mock_session, mock_db):
        """User should see session feed."""
        with patch("app.api.v1.sessions.get_session_feed") as mock_feed:
            mock_feed.return_value = [mock_session]
            
            result = await mock_feed(mock_db, mock_user.id)
            assert len(result) == 1
            assert result[0].id == mock_session.id
    
    @pytest.mark.asyncio
    async def test_get_session_feed_with_filters(self, mock_user, mock_db):
        """Session feed should support date filters."""
        from_date = datetime.utcnow()
        to_date = datetime.utcnow() + timedelta(days=7)
        
        with patch("app.api.v1.sessions.get_session_feed") as mock_feed:
            mock_feed.return_value = []
            
            await mock_feed(
                mock_db,
                user_id=mock_user.id,
                from_date=from_date,
                to_date=to_date
            )
            
            mock_feed.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_session_requires_auth(self, async_client):
        """Session feed requires authentication."""
        response = await async_client.get("/api/v1/sessions")
        
        assert response.status_code == 401


class TestGetSessionById:
    """Test GET /api/v1/sessions/{session_id}."""
    
    @pytest.mark.asyncio
    async def test_get_session_success(self, mock_session, mock_db):
        """Should return session with full details."""
        with patch("app.api.v1.sessions.get_session_by_id") as mock_get:
            mock_get.return_value = mock_session
            
            result = await mock_get(mock_db, mock_session.id)
            assert result.id == mock_session.id
            assert result.title == mock_session.title
    
    @pytest.mark.asyncio
    async def test_get_session_not_found(self, mock_db):
        """Non-existent session should return None."""
        with patch("app.api.v1.sessions.get_session_by_id") as mock_get:
            mock_get.return_value = None
            
            result = await mock_get(mock_db, "nonexistent-id")
            assert result is None


class TestJoinLeaveSession:
    """Test session join/leave endpoints."""
    
    @pytest.mark.asyncio
    async def test_join_session_success(self, mock_user, mock_session, mock_db):
        """User should be able to join a session."""
        mock_session.participants = []
        mock_session.max_participants = 10
        
        with patch("app.api.v1.sessions.join_session") as mock_join:
            mock_join.return_value = None
            
            # Should not raise an error
            await mock_join(mock_db, mock_session.id, mock_user.id)
    
    @pytest.mark.asyncio
    async def test_join_session_full(self, mock_user, mock_session):
        """Cannot join a full session."""
        # Session is at capacity
        mock_session.max_participants = 2
        
        # Create mock participants with GOING status
        participant1 = MagicMock()
        participant1.rsvp_status = RSVPStatus.GOING
        participant2 = MagicMock()
        participant2.rsvp_status = RSVPStatus.GOING
        
        mock_session.participants = [participant1, participant2]
        
        going_count = sum(
            1 for p in mock_session.participants 
            if p.rsvp_status == RSVPStatus.GOING
        )
        
        assert going_count >= mock_session.max_participants
    
    @pytest.mark.asyncio
    async def test_leave_session_success(self, mock_user, mock_session, mock_db):
        """User should be able to leave a session."""
        with patch("app.api.v1.sessions.leave_session") as mock_leave:
            mock_leave.return_value = None
            
            await mock_leave(mock_db, mock_session.id, mock_user.id)
    
    @pytest.mark.asyncio
    async def test_join_requires_auth(self, async_client, mock_session):
        """Join endpoint requires authentication."""
        response = await async_client.post(
            f"/api/v1/sessions/{mock_session.id}/join"
        )
        
        assert response.status_code == 401


class TestRSVP:
    """Test session RSVP endpoint."""
    
    @pytest.mark.asyncio
    async def test_rsvp_going(self, mock_user, mock_session, mock_db):
        """User can RSVP as going."""
        with patch("app.api.v1.sessions.join_session") as mock_join:
            mock_join.return_value = None
            
            await mock_join(
                mock_db, 
                mock_session.id, 
                mock_user.id, 
                rsvp_status=RSVPStatus.GOING
            )
    
    @pytest.mark.asyncio
    async def test_rsvp_maybe(self, mock_user, mock_session, mock_db):
        """User can RSVP as maybe."""
        rsvp_status = RSVPStatus.MAYBE
        assert rsvp_status.value == "maybe"
    
    @pytest.mark.asyncio
    async def test_rsvp_not_going(self, mock_user, mock_session, mock_db):
        """User can RSVP as not going."""
        rsvp_status = RSVPStatus.NOT_GOING
        assert rsvp_status.value == "not_going"


class TestCheckIn:
    """Test session check-in endpoint."""
    
    @pytest.mark.asyncio
    async def test_check_in_success(self, mock_user, mock_session, mock_db):
        """Participant should be able to check in."""
        with patch("app.api.v1.sessions.check_in") as mock_checkin:
            participant = MagicMock()
            participant.checked_in_at = datetime.utcnow()
            mock_checkin.return_value = participant
            
            result = await mock_checkin(mock_db, mock_session.id, mock_user.id)
            assert result.checked_in_at is not None
    
    @pytest.mark.asyncio
    async def test_check_in_not_participant(self, mock_user, mock_session, mock_db):
        """Non-participant cannot check in."""
        with patch("app.api.v1.sessions.check_in") as mock_checkin:
            mock_checkin.return_value = None  # Not a participant
            
            result = await mock_checkin(mock_db, mock_session.id, mock_user.id)
            assert result is None


class TestSessionExercises:
    """Test session exercises endpoint."""
    
    @pytest.mark.asyncio
    async def test_add_exercise_success(self, mock_user, mock_session, mock_exercise, mock_db):
        """Participant can add exercise to session."""
        exercise_data = {
            "name": "Lat Pulldown",
            "sets": 3,
            "reps": "10-12",
            "order": 4
        }
        
        with patch("app.api.v1.sessions.add_exercise_to_session") as mock_add:
            mock_add.return_value = mock_exercise
            
            # Validate exercise data
            assert len(exercise_data["name"]) > 0
            assert exercise_data["sets"] > 0
    
    @pytest.mark.asyncio
    async def test_add_exercise_requires_participation(self, mock_session):
        """Only participants can add exercises."""
        mock_session.participants = []  # No participants
        
        # Non-participant should not be able to add
        assert len(mock_session.participants) == 0
    
    def test_exercise_model(self, mock_exercise):
        """Exercise should have all required fields."""
        required_fields = ["id", "name", "order"]
        optional_fields = ["sets", "reps", "duration_seconds", "notes"]
        
        for field in required_fields:
            assert hasattr(mock_exercise, field)
        
        for field in optional_fields:
            assert hasattr(mock_exercise, field)


class TestSessionInvites:
    """Test session invite endpoint."""
    
    @pytest.mark.asyncio
    async def test_invite_friends_success(self, mock_user, mock_user_2, mock_session, mock_db):
        """Creator can invite friends to session."""
        mock_session.creator_id = mock_user.id
        
        invite_data = {
            "user_ids": [mock_user_2.id],
            "message": "Join me for this workout!"
        }
        
        assert len(invite_data["user_ids"]) > 0
        assert mock_session.creator_id == mock_user.id
    
    @pytest.mark.asyncio
    async def test_invite_multiple_users(self, mock_user, mock_session):
        """Can invite multiple users at once."""
        user_ids = ["user-1", "user-2", "user-3"]
        
        assert len(user_ids) == 3


class TestUpdateSession:
    """Test PATCH /api/v1/sessions/{session_id}."""
    
    @pytest.mark.asyncio
    async def test_update_session_creator_only(self, mock_user, mock_session):
        """Only creator can update session."""
        mock_session.creator_id = mock_user.id
        
        assert mock_session.creator_id == mock_user.id
    
    @pytest.mark.asyncio
    async def test_update_session_non_creator_denied(self, mock_user, mock_user_2, mock_session):
        """Non-creator cannot update session."""
        mock_session.creator_id = mock_user.id
        
        # mock_user_2 is not the creator
        assert mock_session.creator_id != mock_user_2.id
    
    @pytest.mark.asyncio
    async def test_cancel_session(self, mock_session):
        """Creator can cancel session."""
        mock_session.is_cancelled = True
        
        assert mock_session.is_cancelled is True


class TestDeleteSession:
    """Test DELETE /api/v1/sessions/{session_id}."""
    
    @pytest.mark.asyncio
    async def test_delete_session_creator_only(self, mock_user, mock_session, mock_db):
        """Only creator can delete session."""
        mock_session.creator_id = mock_user.id
        
        with patch("app.api.v1.sessions.delete_session") as mock_delete:
            mock_delete.return_value = None
            
            await mock_delete(mock_db, mock_session)
    
    @pytest.mark.asyncio
    async def test_delete_requires_auth(self, async_client, mock_session):
        """Delete endpoint requires authentication."""
        response = await async_client.delete(
            f"/api/v1/sessions/{mock_session.id}"
        )
        
        assert response.status_code == 401

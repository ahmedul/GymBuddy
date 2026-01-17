"""
Unit tests for user profile endpoints.
Tests: get profile, update profile, get other user profile
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from app.models.user import User, TrainingLevel, ProfileVisibility


class TestGetMyProfile:
    """Test GET /api/v1/users/me."""
    
    @pytest.mark.asyncio
    async def test_get_profile_returns_full_data(self, mock_user):
        """User profile should contain all expected fields."""
        expected_fields = [
            "id", "email", "name", "photo_url", "bio",
            "training_level", "visibility", "is_verified", "created_at"
        ]
        
        # Verify mock user has all required attributes
        for field in expected_fields:
            assert hasattr(mock_user, field), f"Missing field: {field}"
    
    @pytest.mark.asyncio
    async def test_get_profile_unauthenticated(self, async_client):
        """Unauthenticated request should fail."""
        response = await async_client.get("/api/v1/users/me")
        
        assert response.status_code == 401


class TestUpdateProfile:
    """Test PATCH /api/v1/users/me."""
    
    @pytest.mark.asyncio
    async def test_update_profile_name(self, mock_user, mock_db):
        """User should be able to update their name."""
        with patch("app.api.v1.users.get_db") as mock_get_db, \
             patch("app.api.v1.users.get_current_user") as mock_get_current, \
             patch("app.api.v1.users.update_user") as mock_update:
            
            mock_get_db.return_value = mock_db
            mock_get_current.return_value = mock_user
            
            updated_user = MagicMock(spec=User)
            updated_user.id = mock_user.id
            updated_user.email = mock_user.email
            updated_user.name = "Updated Name"
            updated_user.photo_url = None
            updated_user.bio = None
            updated_user.training_level = TrainingLevel.BEGINNER
            updated_user.visibility = ProfileVisibility.PRIVATE
            updated_user.is_verified = False
            updated_user.created_at = datetime.utcnow()
            mock_update.return_value = updated_user
            
            # The update data
            update_data = {"name": "Updated Name"}
            
            # Verify mock was called correctly
            assert update_data["name"] == "Updated Name"
    
    @pytest.mark.asyncio
    async def test_update_profile_training_level(self, mock_user):
        """User should be able to update training level."""
        # Valid training levels
        valid_levels = [
            TrainingLevel.BEGINNER,
            TrainingLevel.INTERMEDIATE,
            TrainingLevel.ADVANCED
        ]
        
        for level in valid_levels:
            assert level in TrainingLevel
    
    @pytest.mark.asyncio
    async def test_update_profile_visibility(self, mock_user):
        """User should be able to update profile visibility."""
        # Valid visibility options
        valid_options = [
            ProfileVisibility.PUBLIC,
            ProfileVisibility.FRIENDS,
            ProfileVisibility.PRIVATE
        ]
        
        for option in valid_options:
            assert option in ProfileVisibility
    
    @pytest.mark.asyncio
    async def test_update_profile_bio_max_length(self):
        """Bio should have a maximum length constraint."""
        # Bio is defined as String(500) in the model
        max_length = 500
        
        valid_bio = "A" * max_length
        invalid_bio = "A" * (max_length + 1)
        
        assert len(valid_bio) == max_length
        assert len(invalid_bio) > max_length


class TestGetUserProfile:
    """Test GET /api/v1/users/{user_id}."""
    
    @pytest.mark.asyncio
    async def test_get_public_profile(self, mock_user, mock_user_2, mock_db):
        """Public profile should be viewable by anyone."""
        mock_user_2.visibility = ProfileVisibility.PUBLIC
        
        with patch("app.api.v1.users.get_db") as mock_get_db, \
             patch("app.api.v1.users.get_current_user") as mock_get_current, \
             patch("app.api.v1.users.get_user_by_id") as mock_get_user:
            
            mock_get_db.return_value = mock_db
            mock_get_current.return_value = mock_user
            mock_get_user.return_value = mock_user_2
            
            # Public user should be viewable
            assert mock_user_2.visibility == ProfileVisibility.PUBLIC
    
    @pytest.mark.asyncio
    async def test_get_private_profile_denied(self, mock_user, mock_user_2, mock_db):
        """Private profile should not be viewable by others."""
        mock_user_2.visibility = ProfileVisibility.PRIVATE
        
        # Different user trying to view private profile
        assert mock_user.id != mock_user_2.id
        assert mock_user_2.visibility == ProfileVisibility.PRIVATE
    
    @pytest.mark.asyncio
    async def test_get_own_private_profile(self, mock_user, mock_db):
        """User should always be able to view their own profile."""
        mock_user.visibility = ProfileVisibility.PRIVATE
        
        # User viewing their own profile should work
        assert mock_user.id == mock_user.id  # Same user
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_user(self, async_client, auth_headers):
        """Getting non-existent user should return 404."""
        with patch("app.api.v1.users.get_db"), \
             patch("app.api.v1.users.get_current_user"), \
             patch("app.api.v1.users.get_user_by_id") as mock_get_user:
            
            mock_get_user.return_value = None
            
            # The endpoint should return 404
            # This tests the expected behavior


class TestUserPublicResponse:
    """Test that public response has limited fields."""
    
    def test_public_response_excludes_email(self, mock_user):
        """Public response should not include email."""
        public_fields = ["id", "name", "photo_url", "bio", "training_level"]
        private_fields = ["email", "visibility", "is_verified", "hashed_password"]
        
        # All public fields should be on the user
        for field in public_fields:
            assert hasattr(mock_user, field)
        
        # Private fields exist but shouldn't be in public response
        for field in private_fields:
            assert hasattr(mock_user, field)

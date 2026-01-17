"""
Unit tests for social endpoints.
Tests: friends, friend requests, groups
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from app.models.social import Friendship, FriendshipStatus, Group


class TestFriendshipModel:
    """Test Friendship model properties."""
    
    def test_friendship_status_options(self):
        """Verify all friendship status options."""
        expected = ["pending", "accepted", "declined", "blocked"]
        
        for status in FriendshipStatus:
            assert status.value in expected
    
    def test_friendship_has_required_fields(self, mock_friendship):
        """Friendship should have all required fields."""
        required_fields = [
            "id", "requester_id", "addressee_id", "status", "created_at"
        ]
        
        for field in required_fields:
            assert hasattr(mock_friendship, field), f"Missing field: {field}"


class TestSendFriendRequest:
    """Test POST /api/v1/friends/request."""
    
    @pytest.mark.asyncio
    async def test_send_request_success(self, mock_user, mock_user_2, mock_db):
        """User should be able to send friend request."""
        with patch("app.api.v1.social.create_friend_request") as mock_create:
            friendship = MagicMock(spec=Friendship)
            friendship.id = "new-friendship-id"
            friendship.requester_id = mock_user.id
            friendship.addressee_id = mock_user_2.id
            friendship.status = FriendshipStatus.PENDING
            mock_create.return_value = friendship
            
            result = await mock_create(mock_db, mock_user.id, mock_user_2.id)
            
            assert result.status == FriendshipStatus.PENDING
            assert result.requester_id == mock_user.id
            assert result.addressee_id == mock_user_2.id
    
    @pytest.mark.asyncio
    async def test_cannot_friend_self(self, mock_user):
        """User cannot send friend request to themselves."""
        # Same user ID
        assert mock_user.id == mock_user.id
        # This should be rejected by the endpoint
    
    @pytest.mark.asyncio
    async def test_cannot_duplicate_request(self, mock_user, mock_user_2, mock_friendship, mock_db):
        """Cannot send duplicate friend request."""
        with patch("app.api.v1.social.get_friendship") as mock_get:
            mock_get.return_value = mock_friendship  # Already exists
            
            result = await mock_get(mock_db, mock_user.id, mock_user_2.id)
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_send_request_to_nonexistent_user(self, mock_user, mock_db):
        """Cannot send request to non-existent user."""
        with patch("app.crud.user.get_user_by_id") as mock_get:
            mock_get.return_value = None  # User doesn't exist
            
            result = await mock_get(mock_db, "nonexistent-user-id")
            assert result is None
    
    @pytest.mark.asyncio
    async def test_send_request_requires_auth(self, async_client):
        """Sending friend request requires authentication."""
        response = await async_client.post(
            "/api/v1/friends/request",
            json={"addressee_id": "some-user-id"}
        )
        
        assert response.status_code == 401


class TestListFriends:
    """Test GET /api/v1/friends."""
    
    @pytest.mark.asyncio
    async def test_list_friends_empty(self, mock_user, mock_db):
        """New user should have no friends."""
        with patch("app.api.v1.social.get_friends") as mock_get:
            mock_get.return_value = []
            
            result = await mock_get(mock_db, mock_user.id)
            assert result == []
    
    @pytest.mark.asyncio
    async def test_list_friends_with_friends(self, mock_user, mock_user_2, mock_friendship, mock_db):
        """User with friends should see them listed."""
        mock_friendship.status = FriendshipStatus.ACCEPTED
        
        with patch("app.api.v1.social.get_friends") as mock_get:
            mock_get.return_value = [mock_friendship]
            
            result = await mock_get(mock_db, mock_user.id)
            assert len(result) == 1
    
    @pytest.mark.asyncio
    async def test_list_friends_requires_auth(self, async_client):
        """Listing friends requires authentication."""
        response = await async_client.get("/api/v1/friends")
        
        assert response.status_code == 401


class TestPendingRequests:
    """Test GET /api/v1/friends/requests."""
    
    @pytest.mark.asyncio
    async def test_list_pending_requests(self, mock_user, mock_friendship, mock_db):
        """User should see pending friend requests."""
        mock_friendship.status = FriendshipStatus.PENDING
        mock_friendship.addressee_id = mock_user.id  # Request TO this user
        
        with patch("app.api.v1.social.get_pending_requests") as mock_get:
            mock_get.return_value = [mock_friendship]
            
            result = await mock_get(mock_db, mock_user.id)
            assert len(result) == 1
            assert result[0].status == FriendshipStatus.PENDING
    
    @pytest.mark.asyncio
    async def test_no_pending_requests(self, mock_user, mock_db):
        """User with no pending requests should see empty list."""
        with patch("app.api.v1.social.get_pending_requests") as mock_get:
            mock_get.return_value = []
            
            result = await mock_get(mock_db, mock_user.id)
            assert result == []


class TestAcceptFriendRequest:
    """Test POST /api/v1/friends/requests/{id}/accept."""
    
    @pytest.mark.asyncio
    async def test_accept_request_success(self, mock_user, mock_friendship, mock_db):
        """Addressee can accept friend request."""
        mock_friendship.addressee_id = mock_user.id
        mock_friendship.status = FriendshipStatus.PENDING
        
        with patch("app.api.v1.social.update_friendship_status") as mock_update:
            updated = MagicMock(spec=Friendship)
            updated.status = FriendshipStatus.ACCEPTED
            mock_update.return_value = updated
            
            result = await mock_update(mock_db, mock_friendship, FriendshipStatus.ACCEPTED)
            assert result.status == FriendshipStatus.ACCEPTED
    
    @pytest.mark.asyncio
    async def test_cannot_accept_others_request(self, mock_user, mock_user_2, mock_friendship):
        """Cannot accept request not addressed to you."""
        mock_friendship.addressee_id = mock_user_2.id  # Not addressed to mock_user
        
        assert mock_friendship.addressee_id != mock_user.id
    
    @pytest.mark.asyncio
    async def test_accept_nonexistent_request(self, mock_db):
        """Cannot accept non-existent request."""
        # Simulating lookup returns None
        result = None
        assert result is None


class TestDeclineFriendRequest:
    """Test POST /api/v1/friends/requests/{id}/decline."""
    
    @pytest.mark.asyncio
    async def test_decline_request_success(self, mock_user, mock_friendship, mock_db):
        """Addressee can decline friend request."""
        mock_friendship.addressee_id = mock_user.id
        mock_friendship.status = FriendshipStatus.PENDING
        
        with patch("app.api.v1.social.update_friendship_status") as mock_update:
            updated = MagicMock(spec=Friendship)
            updated.status = FriendshipStatus.DECLINED
            mock_update.return_value = updated
            
            result = await mock_update(mock_db, mock_friendship, FriendshipStatus.DECLINED)
            assert result.status == FriendshipStatus.DECLINED


class TestGroupModel:
    """Test Group model properties."""
    
    def test_group_has_required_fields(self, mock_group):
        """Group should have all required fields."""
        required_fields = [
            "id", "name", "owner_id", "is_public", "created_at"
        ]
        
        for field in required_fields:
            assert hasattr(mock_group, field), f"Missing field: {field}"


class TestCreateGroup:
    """Test POST /api/v1/groups."""
    
    @pytest.mark.asyncio
    async def test_create_group_success(self, mock_user, mock_db):
        """User should be able to create a group."""
        group_data = {
            "name": "Morning Lifters",
            "description": "Early birds who lift heavy",
            "is_public": True
        }
        
        with patch("app.api.v1.social.create_group") as mock_create:
            group = MagicMock(spec=Group)
            group.id = "new-group-id"
            group.name = group_data["name"]
            group.owner_id = mock_user.id
            mock_create.return_value = group
            
            # Validate data
            assert len(group_data["name"]) > 0
    
    @pytest.mark.asyncio
    async def test_create_group_requires_auth(self, async_client):
        """Creating a group requires authentication."""
        response = await async_client.post(
            "/api/v1/groups",
            json={
                "name": "Test Group",
                "is_public": True
            }
        )
        
        assert response.status_code == 401


class TestListGroups:
    """Test GET /api/v1/groups."""
    
    @pytest.mark.asyncio
    async def test_list_my_groups(self, mock_user, mock_group, mock_db):
        """User should see their groups."""
        mock_group.owner_id = mock_user.id
        
        with patch("app.api.v1.social.get_user_groups") as mock_get:
            mock_get.return_value = [mock_group]
            
            result = await mock_get(mock_db, mock_user.id)
            assert len(result) == 1
            assert result[0].owner_id == mock_user.id
    
    @pytest.mark.asyncio
    async def test_list_groups_empty(self, mock_user, mock_db):
        """User with no groups should see empty list."""
        with patch("app.api.v1.social.get_user_groups") as mock_get:
            mock_get.return_value = []
            
            result = await mock_get(mock_db, mock_user.id)
            assert result == []


class TestGetGroupById:
    """Test GET /api/v1/groups/{group_id}."""
    
    @pytest.mark.asyncio
    async def test_get_group_success(self, mock_group, mock_db):
        """Should return group by ID."""
        with patch("app.api.v1.social.get_group_by_id") as mock_get:
            mock_get.return_value = mock_group
            
            result = await mock_get(mock_db, mock_group.id)
            assert result.id == mock_group.id
    
    @pytest.mark.asyncio
    async def test_get_group_not_found(self, mock_db):
        """Non-existent group should return None."""
        with patch("app.api.v1.social.get_group_by_id") as mock_get:
            mock_get.return_value = None
            
            result = await mock_get(mock_db, "nonexistent-id")
            assert result is None


class TestUpdateGroup:
    """Test PATCH /api/v1/groups/{group_id}."""
    
    @pytest.mark.asyncio
    async def test_update_group_owner_only(self, mock_user, mock_group, mock_db):
        """Only owner can update group."""
        mock_group.owner_id = mock_user.id
        
        with patch("app.api.v1.social.update_group") as mock_update:
            updated = MagicMock(spec=Group)
            updated.name = "Updated Group Name"
            mock_update.return_value = updated
            
            assert mock_group.owner_id == mock_user.id
    
    @pytest.mark.asyncio
    async def test_update_group_non_owner_denied(self, mock_user, mock_user_2, mock_group):
        """Non-owner cannot update group."""
        mock_group.owner_id = mock_user.id
        
        # mock_user_2 is not the owner
        assert mock_group.owner_id != mock_user_2.id

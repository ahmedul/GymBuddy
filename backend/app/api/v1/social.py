from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user
from app.crud.social import (
    get_friendship, create_friend_request, update_friendship_status,
    get_friends, get_pending_requests,
    get_group_by_id, create_group, update_group, get_user_groups
)
from app.crud.user import get_user_by_id
from app.schemas.social import (
    FriendRequest, FriendshipResponse, FriendResponse,
    GroupCreate, GroupUpdate, GroupResponse
)
from app.models.user import User
from app.models.social import FriendshipStatus

router = APIRouter(tags=["social"])


# === Friends ===

@router.post("/friends/request", response_model=FriendshipResponse)
async def send_friend_request(
    request: FriendRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send a friend request to another user."""
    if request.addressee_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send friend request to yourself"
        )
    
    # Check if user exists
    addressee = await get_user_by_id(db, request.addressee_id)
    if not addressee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check existing friendship
    existing = await get_friendship(db, current_user.id, request.addressee_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Friendship already exists"
        )
    
    friendship = await create_friend_request(db, current_user.id, request.addressee_id)
    return friendship


@router.get("/friends", response_model=List[FriendResponse])
async def list_friends(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of all friends."""
    friendships = await get_friends(db, current_user.id)
    
    friends = []
    for f in friendships:
        friend_id = f.addressee_id if f.requester_id == current_user.id else f.requester_id
        friend_user = await get_user_by_id(db, friend_id)
        if friend_user:
            friends.append(FriendResponse(
                user=friend_user,
                friendship_id=f.id,
                since=f.updated_at
            ))
    
    return friends


@router.get("/friends/requests", response_model=List[FriendshipResponse])
async def list_pending_requests(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get pending friend requests."""
    requests = await get_pending_requests(db, current_user.id)
    return requests


@router.post("/friends/requests/{friendship_id}/accept", response_model=FriendshipResponse)
async def accept_friend_request(
    friendship_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Accept a friend request."""
    from sqlalchemy import select
    from app.models.social import Friendship
    
    result = await db.execute(select(Friendship).where(Friendship.id == friendship_id))
    friendship = result.scalar_one_or_none()
    
    if not friendship or friendship.addressee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friend request not found"
        )
    
    updated = await update_friendship_status(db, friendship, FriendshipStatus.ACCEPTED)
    return updated


@router.post("/friends/requests/{friendship_id}/decline", response_model=FriendshipResponse)
async def decline_friend_request(
    friendship_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Decline a friend request."""
    from sqlalchemy import select
    from app.models.social import Friendship
    
    result = await db.execute(select(Friendship).where(Friendship.id == friendship_id))
    friendship = result.scalar_one_or_none()
    
    if not friendship or friendship.addressee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friend request not found"
        )
    
    updated = await update_friendship_status(db, friendship, FriendshipStatus.DECLINED)
    return updated


# === Groups ===

@router.post("/groups", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_new_group(
    group_in: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new group."""
    group = await create_group(db, current_user.id, group_in)
    return group


@router.get("/groups", response_model=List[GroupResponse])
async def list_my_groups(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get groups owned by current user."""
    groups = await get_user_groups(db, current_user.id)
    return groups


@router.get("/groups/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a group by ID."""
    group = await get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    return group


@router.patch("/groups/{group_id}", response_model=GroupResponse)
async def update_group_info(
    group_id: str,
    group_in: GroupUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a group (owner only)."""
    group = await get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    if group.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner can update this group"
        )
    
    updated_group = await update_group(db, group, group_in)
    return updated_group

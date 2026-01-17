from typing import List, Optional
from uuid import uuid4
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.social import Friendship, FriendshipStatus, Group
from app.models.user import User
from app.schemas.social import GroupCreate, GroupUpdate


# Friendships
async def get_friendship(
    db: AsyncSession, 
    user_id: str, 
    other_user_id: str
) -> Optional[Friendship]:
    result = await db.execute(
        select(Friendship).where(
            or_(
                and_(Friendship.requester_id == user_id, Friendship.addressee_id == other_user_id),
                and_(Friendship.requester_id == other_user_id, Friendship.addressee_id == user_id)
            )
        )
    )
    return result.scalar_one_or_none()


async def create_friend_request(
    db: AsyncSession,
    requester_id: str,
    addressee_id: str
) -> Friendship:
    friendship = Friendship(
        id=str(uuid4()),
        requester_id=requester_id,
        addressee_id=addressee_id,
        status=FriendshipStatus.PENDING
    )
    db.add(friendship)
    await db.flush()
    await db.refresh(friendship)
    return friendship


async def update_friendship_status(
    db: AsyncSession,
    friendship: Friendship,
    status: FriendshipStatus
) -> Friendship:
    friendship.status = status
    await db.flush()
    await db.refresh(friendship)
    return friendship


async def get_friends(db: AsyncSession, user_id: str) -> List[Friendship]:
    result = await db.execute(
        select(Friendship).where(
            and_(
                or_(
                    Friendship.requester_id == user_id,
                    Friendship.addressee_id == user_id
                ),
                Friendship.status == FriendshipStatus.ACCEPTED
            )
        )
    )
    return result.scalars().all()


async def get_pending_requests(db: AsyncSession, user_id: str) -> List[Friendship]:
    result = await db.execute(
        select(Friendship).where(
            and_(
                Friendship.addressee_id == user_id,
                Friendship.status == FriendshipStatus.PENDING
            )
        )
    )
    return result.scalars().all()


# Groups
async def get_group_by_id(db: AsyncSession, group_id: str) -> Optional[Group]:
    result = await db.execute(select(Group).where(Group.id == group_id))
    return result.scalar_one_or_none()


async def create_group(db: AsyncSession, owner_id: str, group_in: GroupCreate) -> Group:
    group = Group(
        id=str(uuid4()),
        owner_id=owner_id,
        **group_in.model_dump()
    )
    db.add(group)
    await db.flush()
    await db.refresh(group)
    return group


async def update_group(db: AsyncSession, group: Group, group_in: GroupUpdate) -> Group:
    update_data = group_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)
    await db.flush()
    await db.refresh(group)
    return group


async def get_user_groups(db: AsyncSession, user_id: str) -> List[Group]:
    result = await db.execute(
        select(Group).where(Group.owner_id == user_id)
    )
    return result.scalars().all()

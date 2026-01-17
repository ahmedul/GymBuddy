from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import Session, SessionParticipant, SessionExercise, SessionVisibility, RSVPStatus
from app.models.social import Friendship, FriendshipStatus
from app.schemas.session import SessionCreate, SessionUpdate, ExerciseCreate


async def get_session_by_id(db: AsyncSession, session_id: str) -> Optional[Session]:
    result = await db.execute(
        select(Session)
        .options(
            selectinload(Session.creator),
            selectinload(Session.gym),
            selectinload(Session.participants).selectinload(SessionParticipant.user),
            selectinload(Session.exercises)
        )
        .where(Session.id == session_id)
    )
    return result.scalar_one_or_none()


async def create_session(db: AsyncSession, creator_id: str, session_in: SessionCreate) -> Session:
    session = Session(
        id=str(uuid4()),
        creator_id=creator_id,
        title=session_in.title,
        description=session_in.description,
        gym_id=session_in.gym_id,
        scheduled_at=session_in.scheduled_at,
        duration_minutes=session_in.duration_minutes,
        visibility=session_in.visibility,
        group_id=session_in.group_id,
        max_participants=session_in.max_participants,
        is_recurring=session_in.is_recurring,
        recurrence_rule=session_in.recurrence_rule
    )
    db.add(session)
    
    # Add exercises
    for i, exercise_in in enumerate(session_in.exercises):
        exercise = SessionExercise(
            id=str(uuid4()),
            session_id=session.id,
            name=exercise_in.name,
            sets=exercise_in.sets,
            reps=exercise_in.reps,
            duration_seconds=exercise_in.duration_seconds,
            notes=exercise_in.notes,
            order=exercise_in.order if exercise_in.order else i
        )
        db.add(exercise)
    
    # Creator auto-joins
    participant = SessionParticipant(
        id=str(uuid4()),
        session_id=session.id,
        user_id=creator_id,
        rsvp_status=RSVPStatus.GOING
    )
    db.add(participant)
    
    await db.flush()
    return await get_session_by_id(db, session.id)


async def update_session(db: AsyncSession, session: Session, session_in: SessionUpdate) -> Session:
    update_data = session_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(session, field, value)
    await db.flush()
    await db.refresh(session)
    return session


async def delete_session(db: AsyncSession, session: Session) -> bool:
    await db.delete(session)
    await db.flush()
    return True


async def get_session_feed(
    db: AsyncSession,
    user_id: str,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    include_public: bool = True,
    limit: int = 50
) -> List[Session]:
    """Get sessions visible to user (friends' sessions + public)"""
    
    # Get user's friend IDs
    friends_result = await db.execute(
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
    friendships = friends_result.scalars().all()
    friend_ids = [
        f.addressee_id if f.requester_id == user_id else f.requester_id
        for f in friendships
    ]
    
    # Build query
    stmt = select(Session).options(
        selectinload(Session.creator),
        selectinload(Session.gym),
        selectinload(Session.participants)
    )
    
    # Visibility conditions
    visibility_conditions = [
        Session.creator_id == user_id,  # Own sessions
    ]
    
    if friend_ids:
        visibility_conditions.append(
            and_(
                Session.creator_id.in_(friend_ids),
                Session.visibility.in_([SessionVisibility.FRIENDS, SessionVisibility.PUBLIC])
            )
        )
    
    if include_public:
        visibility_conditions.append(Session.visibility == SessionVisibility.PUBLIC)
    
    stmt = stmt.where(
        and_(
            or_(*visibility_conditions),
            Session.is_cancelled == False
        )
    )
    
    if from_date:
        stmt = stmt.where(Session.scheduled_at >= from_date)
    if to_date:
        stmt = stmt.where(Session.scheduled_at <= to_date)
    
    stmt = stmt.order_by(Session.scheduled_at).limit(limit)
    
    result = await db.execute(stmt)
    return result.scalars().all()


async def join_session(
    db: AsyncSession,
    session_id: str,
    user_id: str,
    rsvp_status: RSVPStatus = RSVPStatus.GOING,
    invited_by_id: Optional[str] = None,
    invite_message: Optional[str] = None
) -> SessionParticipant:
    # Check if already participant
    result = await db.execute(
        select(SessionParticipant).where(
            SessionParticipant.session_id == session_id,
            SessionParticipant.user_id == user_id
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.rsvp_status = rsvp_status
        await db.flush()
        await db.refresh(existing)
        return existing
    
    participant = SessionParticipant(
        id=str(uuid4()),
        session_id=session_id,
        user_id=user_id,
        rsvp_status=rsvp_status,
        invited_by_id=invited_by_id,
        invite_message=invite_message
    )
    db.add(participant)
    await db.flush()
    await db.refresh(participant)
    return participant


async def leave_session(db: AsyncSession, session_id: str, user_id: str) -> bool:
    result = await db.execute(
        select(SessionParticipant).where(
            SessionParticipant.session_id == session_id,
            SessionParticipant.user_id == user_id
        )
    )
    participant = result.scalar_one_or_none()
    if participant:
        await db.delete(participant)
        await db.flush()
        return True
    return False


async def check_in(db: AsyncSession, session_id: str, user_id: str) -> Optional[SessionParticipant]:
    result = await db.execute(
        select(SessionParticipant).where(
            SessionParticipant.session_id == session_id,
            SessionParticipant.user_id == user_id
        )
    )
    participant = result.scalar_one_or_none()
    if participant:
        participant.checked_in = True
        participant.checked_in_at = datetime.utcnow()
        await db.flush()
        await db.refresh(participant)
        return participant
    return None


async def add_exercise_to_session(
    db: AsyncSession,
    session_id: str,
    exercise_in: ExerciseCreate
) -> SessionExercise:
    exercise = SessionExercise(
        id=str(uuid4()),
        session_id=session_id,
        **exercise_in.model_dump()
    )
    db.add(exercise)
    await db.flush()
    await db.refresh(exercise)
    return exercise

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user
from app.crud.session import (
    get_session_by_id, create_session, update_session, delete_session,
    get_session_feed, join_session, leave_session, check_in,
    add_exercise_to_session
)
from app.crud.gym import get_gym_by_id
from app.schemas.session import (
    SessionCreate, SessionUpdate, SessionResponse, SessionDetailResponse,
    SessionInvite, RSVPRequest, ExerciseCreate, ExerciseResponse
)
from app.models.user import User
from app.models.session import RSVPStatus

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("", response_model=List[SessionResponse])
async def list_sessions(
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    include_public: bool = Query(True),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get session feed (friends' sessions + public)."""
    sessions = await get_session_feed(
        db,
        user_id=current_user.id,
        from_date=from_date,
        to_date=to_date,
        include_public=include_public
    )
    
    # Add participant count
    result = []
    for session in sessions:
        session_dict = {
            "id": session.id,
            "title": session.title,
            "description": session.description,
            "gym": session.gym,
            "scheduled_at": session.scheduled_at,
            "duration_minutes": session.duration_minutes,
            "visibility": session.visibility,
            "max_participants": session.max_participants,
            "creator": session.creator,
            "is_recurring": session.is_recurring,
            "is_cancelled": session.is_cancelled,
            "participant_count": len(session.participants),
            "created_at": session.created_at
        }
        result.append(SessionResponse(**session_dict))
    
    return result


@router.post("", response_model=SessionDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_new_session(
    session_in: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new workout session."""
    # Verify gym exists
    gym = await get_gym_by_id(db, session_in.gym_id)
    if not gym:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gym not found"
        )
    
    session = await create_session(db, current_user.id, session_in)
    return _session_to_detail_response(session)


@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a session by ID."""
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # TODO: Check visibility permissions
    
    return _session_to_detail_response(session)


@router.patch("/{session_id}", response_model=SessionDetailResponse)
async def update_session_info(
    session_id: str,
    session_in: SessionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a session (creator only)."""
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the creator can update this session"
        )
    
    updated = await update_session(db, session, session_in)
    return _session_to_detail_response(await get_session_by_id(db, session_id))


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session_endpoint(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a session (creator only)."""
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the creator can delete this session"
        )
    
    await delete_session(db, session)


@router.post("/{session_id}/join", status_code=status.HTTP_204_NO_CONTENT)
async def join_session_endpoint(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Join a session."""
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Check capacity
    if session.max_participants:
        going_count = sum(1 for p in session.participants if p.rsvp_status == RSVPStatus.GOING)
        if going_count >= session.max_participants:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is full"
            )
    
    await join_session(db, session_id, current_user.id)


@router.post("/{session_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_session_endpoint(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Leave a session."""
    await leave_session(db, session_id, current_user.id)


@router.post("/{session_id}/rsvp")
async def update_rsvp(
    session_id: str,
    rsvp: RSVPRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update RSVP status."""
    await join_session(db, session_id, current_user.id, rsvp_status=rsvp.status)
    return {"status": "updated"}


@router.post("/{session_id}/check-in")
async def check_in_endpoint(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Check in to a session."""
    participant = await check_in(db, session_id, current_user.id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must join the session first"
        )
    return {"checked_in": True, "checked_in_at": participant.checked_in_at}


@router.post("/{session_id}/invite", status_code=status.HTTP_204_NO_CONTENT)
async def invite_to_session(
    session_id: str,
    invite: SessionInvite,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Invite users to a session."""
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    for user_id in invite.user_ids:
        await join_session(
            db,
            session_id,
            user_id,
            rsvp_status=RSVPStatus.MAYBE,
            invited_by_id=current_user.id,
            invite_message=invite.message
        )


@router.post("/{session_id}/exercises", response_model=ExerciseResponse)
async def add_exercise(
    session_id: str,
    exercise_in: ExerciseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add an exercise to a session."""
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Check if user is participant or creator
    is_participant = any(p.user_id == current_user.id for p in session.participants)
    if not is_participant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only participants can add exercises"
        )
    
    exercise = await add_exercise_to_session(db, session_id, exercise_in)
    return exercise


def _session_to_detail_response(session) -> SessionDetailResponse:
    """Convert session model to detailed response."""
    return SessionDetailResponse(
        id=session.id,
        title=session.title,
        description=session.description,
        gym=session.gym,
        scheduled_at=session.scheduled_at,
        duration_minutes=session.duration_minutes,
        visibility=session.visibility,
        max_participants=session.max_participants,
        creator=session.creator,
        is_recurring=session.is_recurring,
        is_cancelled=session.is_cancelled,
        participant_count=len(session.participants),
        created_at=session.created_at,
        participants=session.participants,
        exercises=session.exercises,
        group_id=session.group_id
    )

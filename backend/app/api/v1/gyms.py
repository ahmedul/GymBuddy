from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import get_current_user
from app.crud.gym import (
    get_gym_by_id, create_gym, search_gyms,
    add_favorite_gym, remove_favorite_gym, get_favorite_gyms
)
from app.schemas.gym import GymCreate, GymResponse
from app.models.user import User

router = APIRouter(prefix="/gyms", tags=["gyms"])


@router.get("", response_model=List[GymResponse])
async def list_gyms(
    q: Optional[str] = Query(None, description="Search query"),
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
    radius: float = Query(10.0, description="Search radius in km"),
    db: AsyncSession = Depends(get_db)
):
    """Search for gyms by name or location."""
    gyms = await search_gyms(
        db,
        query=q,
        latitude=lat,
        longitude=lon,
        radius_km=radius
    )
    return gyms


@router.post("", response_model=GymResponse, status_code=status.HTTP_201_CREATED)
async def create_custom_gym(
    gym_in: GymCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a custom location (gym/park/etc)."""
    gym = await create_gym(db, gym_in, created_by_id=current_user.id)
    return gym


@router.get("/favorites", response_model=List[GymResponse])
async def list_favorite_gyms(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's favorite gyms."""
    gyms = await get_favorite_gyms(db, current_user.id)
    return gyms


@router.post("/favorites/{gym_id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_gym_to_favorites(
    gym_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add a gym to favorites."""
    gym = await get_gym_by_id(db, gym_id)
    if not gym:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gym not found"
        )
    
    await add_favorite_gym(db, current_user.id, gym_id)


@router.delete("/favorites/{gym_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_gym_from_favorites(
    gym_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove a gym from favorites."""
    await remove_favorite_gym(db, current_user.id, gym_id)


@router.get("/{gym_id}", response_model=GymResponse)
async def get_gym(
    gym_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a gym by ID."""
    gym = await get_gym_by_id(db, gym_id)
    if not gym:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gym not found"
        )
    return gym

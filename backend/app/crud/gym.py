from typing import List, Optional
from uuid import uuid4
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gym import Gym
from app.models.user import UserFavoriteGym
from app.schemas.gym import GymCreate, GymUpdate


async def get_gym_by_id(db: AsyncSession, gym_id: str) -> Optional[Gym]:
    result = await db.execute(select(Gym).where(Gym.id == gym_id))
    return result.scalar_one_or_none()


async def create_gym(db: AsyncSession, gym_in: GymCreate, created_by_id: Optional[str] = None) -> Gym:
    gym = Gym(
        id=str(uuid4()),
        is_custom=created_by_id is not None,
        created_by_id=created_by_id,
        **gym_in.model_dump()
    )
    db.add(gym)
    await db.flush()
    await db.refresh(gym)
    return gym


async def update_gym(db: AsyncSession, gym: Gym, gym_in: GymUpdate) -> Gym:
    update_data = gym_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(gym, field, value)
    await db.flush()
    await db.refresh(gym)
    return gym


async def search_gyms(
    db: AsyncSession,
    query: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_km: float = 10.0,
    limit: int = 20
) -> List[Gym]:
    stmt = select(Gym)
    
    if query:
        stmt = stmt.where(Gym.name.ilike(f"%{query}%"))
    
    if latitude is not None and longitude is not None:
        # Simple distance calculation (Haversine would be more accurate)
        # This is a rough approximation for nearby filtering
        lat_range = radius_km / 111.0  # ~111km per degree latitude
        lon_range = radius_km / (111.0 * abs(func.cos(func.radians(latitude))))
        
        stmt = stmt.where(
            Gym.latitude.between(latitude - lat_range, latitude + lat_range),
            Gym.longitude.between(longitude - lon_range, longitude + lon_range)
        )
    
    stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def add_favorite_gym(db: AsyncSession, user_id: str, gym_id: str) -> UserFavoriteGym:
    favorite = UserFavoriteGym(user_id=user_id, gym_id=gym_id)
    db.add(favorite)
    await db.flush()
    return favorite


async def remove_favorite_gym(db: AsyncSession, user_id: str, gym_id: str) -> bool:
    result = await db.execute(
        select(UserFavoriteGym).where(
            UserFavoriteGym.user_id == user_id,
            UserFavoriteGym.gym_id == gym_id
        )
    )
    favorite = result.scalar_one_or_none()
    if favorite:
        await db.delete(favorite)
        await db.flush()
        return True
    return False


async def get_favorite_gyms(db: AsyncSession, user_id: str) -> List[Gym]:
    result = await db.execute(
        select(Gym)
        .join(UserFavoriteGym)
        .where(UserFavoriteGym.user_id == user_id)
    )
    return result.scalars().all()

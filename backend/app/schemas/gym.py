from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class GymBase(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float


class GymCreate(GymBase):
    phone: Optional[str] = None
    website: Optional[str] = None
    google_place_id: Optional[str] = None


class GymUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    photo_url: Optional[str] = None


class GymResponse(BaseModel):
    id: str
    name: str
    address: str
    latitude: float
    longitude: float
    phone: Optional[str] = None
    website: Optional[str] = None
    photo_url: Optional[str] = None
    is_custom: bool
    created_at: datetime

    class Config:
        from_attributes = True


class GymSearchQuery(BaseModel):
    query: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: float = 10.0

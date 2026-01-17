from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.social import router as social_router
from app.api.v1.gyms import router as gyms_router
from app.api.v1.sessions import router as sessions_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(social_router)
router.include_router(gyms_router)
router.include_router(sessions_router)

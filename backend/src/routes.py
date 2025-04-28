from fastapi import APIRouter

from packages.auth import auth_router
from packages.protected import protected_router


router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(protected_router, prefix="/protected", tags=["Protected"])

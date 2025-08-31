from fastapi import APIRouter
from app.endpoints.v1.auth_routes import router as auth_router
from app.endpoints.v1.polis_routes import router as polis_router
from app.endpoints.v1.user_routes import router as user_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router, prefix="/auth")
router.include_router(polis_router)
router.include_router(user_router, prefix="/users")

from fastapi import APIRouter
from .routers import router as router_db

router = APIRouter()
router.include_router(router_db)
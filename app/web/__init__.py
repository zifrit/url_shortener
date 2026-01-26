from fastapi import APIRouter
from web.main_views import router as main_router

router = APIRouter(
    include_in_schema=False,
)
router.include_router(main_router)

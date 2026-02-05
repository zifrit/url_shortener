from fastapi import APIRouter, Depends

from services.dependencies.other import username_password_auth
from web.film import router as film_router
from web.main_views import router as main_router
from web.short_url import router as short_url_router

router = APIRouter(dependencies=[Depends(username_password_auth)])
router.include_router(main_router)
router.include_router(short_url_router)
router.include_router(film_router)

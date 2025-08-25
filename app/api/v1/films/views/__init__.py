__all__ = ("router", "details_router")
from .details import router as details_router
from .list import router

router.include_router(details_router)

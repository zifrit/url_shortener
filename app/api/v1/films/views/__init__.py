__all__ = ("details_router", "router")
from .details import router as details_router
from .list import router

router.include_router(details_router)

from fastapi import APIRouter, status

from .v1 import router as v1_router

router = APIRouter(
    prefix="/api",
    responses={
        # status.HTTP_204_NO_CONTENT: None,
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid token or incorrect Password or Username",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid token or incorrect Password or Username",
                    },
                },
            },
        },
    },
)

router.include_router(v1_router)

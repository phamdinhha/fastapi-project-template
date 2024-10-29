from fastapi import APIRouter, Depends
from app.api.http.products import router as products_router
from app.middleware.auth import verify_token

api_router = APIRouter(
    prefix="/api/v1",
    dependencies=[Depends(verify_token)]
)
api_router.include_router(products_router)

from fastapi import FastAPI
from app.api.http.products import router as products_router

api_router = FastAPI()
api_router.include_router(products_router)

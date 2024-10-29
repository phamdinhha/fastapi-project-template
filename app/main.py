from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.database.postgres import get_session

app = FastAPI(
    title=settings.SERVER_NAME,
    openapi_url=f"/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    db_connection = await get_session()
    await db_connection.execute(text("SELECT 1"))
    return {"status": "ok"}

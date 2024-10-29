from fastapi import FastAPI, Request, Depends
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.settings import settings
from sqlalchemy.sql import text
from app.database.postgres import get_session
from app.middleware.http_error_handler import HTTPErrorHandler
from app.middleware.auth import Auth


app = FastAPI(
    title=settings.SERVER_NAME,
    openapi_url=f"/openapi.json",
    dependencies=[Depends(Auth.verify_token)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    handler = HTTPErrorHandler.handle_exceptions(lambda: None)
    return await handler(request, exc)

# Health check endpoint
@app.get("/health")
async def health_check():
    db_connection = await get_session()
    await db_connection.execute(text("SELECT 1"))
    return {"status": "ok"}

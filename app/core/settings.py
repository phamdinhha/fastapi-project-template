from typing import Any, Dict, Optional
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    SERVER_PORT: int
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_NAME: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    DB_ENGINE_POOL_SIZE: str

    PUBLIC_AUTH_JWKS_URL: str
    PUBLIC_AUTH_KID: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # Change to Oracle database
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"postgresql+asyncpg://{values.get('DB_USER')}:{values.get('DB_PASSWORD')}@{values.get('DB_HOST')}:{values.get('DB_PORT')}/{values.get('DB_NAME')}"

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings(_env_file='.env')

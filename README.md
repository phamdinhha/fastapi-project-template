# FastAPI Service Template

A modern FastAPI service template with async SQLAlchemy, PostgreSQL, and custom middleware for authentication and error handling.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **Async SQLAlchemy** - Async ORM for database operations
- **PostgreSQL** - Robust, production-ready database
- **Alembic** - Database migration tool
- **Custom Middleware**
  - Authentication with JWT
  - Global HTTP exception handling
- **Poetry** - Dependency management
- **Pytest** - Testing framework with async support
- **Docker** - Containerization for development and production
- **Uvicorn** - ASGI server for FastAPI

## Prerequisites

- Python 3.12+
- PostgreSQL
- Poetry

## Installation

1. **Clone the repository**
```
git clone git@github.com:phamdinhha/fastapi-project-template.git
```

2. **Set up environment variables**
```
cp .env.example .env
```

3. **Set up environment variables**

Configure your `.env` file:
Server Settings
SERVER_NAME=FastAPI Service
SERVER_HOST=localhost
SERVER_PORT=8000
Database Settings
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_db
Authentication
PUBLIC_AUTH_JWKS_URL=your_jwks_url
PUBLIC_AUTH_KID=your_kid
Logging
LOG_LEVEL=INFO

### Docker compose for setting up local development environment
```
mkdir -p data/postgres_data
mkdir -p data/minio_data
docker compose up --build
```
### Build your image
```
docker build -t fastapi-project-template -f Dockerfile .
```

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, engine
from .routers import health, url


@asynccontextmanager
async def lifespan(_: FastAPI):
    # At startup

    app_env = os.getenv("APP_ENV", "dev")
    # Only create tables if not in test environment
    if app_env != "test":
        Base.metadata.create_all(bind=engine)

    yield
    # Before shutdown


# Initialize the FastAPI application
app = FastAPI(lifespan=lifespan)


# Include Routers
# 1) Health endpoints under "/health"
app.include_router(health.router)

# 2) The main URL operations under "/api/urls"
app.include_router(url.router)

# 3) The redirect operation at the root path "/{short_code}"
app.include_router(url.redirect_router)

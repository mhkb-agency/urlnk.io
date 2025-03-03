from fastapi import FastAPI

from .database import Base, engine
from .routers import health, url

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

# Include Routers
app.include_router(health.router)
app.include_router(url.router)

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class HealthCheck(BaseModel):
    status: str

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")

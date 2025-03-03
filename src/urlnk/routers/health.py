from fastapi import APIRouter, status
from ..models import HealthCheck

router = APIRouter(
    prefix="/health",
    tags=["healthcheck"]
)

@router.get(
    "",
    summary="Perform a Health Check",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    A simple health check endpoint.
    """
    return HealthCheck(status="OK")

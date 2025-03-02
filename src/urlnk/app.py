import random
import string

from fastapi import FastAPI, status
from pydantic import BaseModel, HttpUrl, TypeAdapter

app = FastAPI()


# ------------------------------
# Health Check Endpoint
# ------------------------------
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
    """
    A simple health check endpoint.
    """
    return HealthCheck(status="OK")


# ------------------------------
# URL Shortening Endpoints
# ------------------------------
class ShortenRequest(BaseModel):
    """
    Request model for URL shortening.
    Expects a valid URL to be provided in the 'long_url' field.
    """
    long_url: HttpUrl


class ShortenResponse(BaseModel):
    """
    Response model for URL shortening.
    Returns the generated short URL.
    """
    short_url: HttpUrl


# In-memory store for mapping short codes to long URLs.
# TODO: In production, use a persistent data store.
url_mapping: dict[str, HttpUrl] = {}


def generate_short_code(length: int = 6) -> str:
    """
    Generates a random string of letters and digits of the given length.

    Args:
        length (int): The length of the short code to generate.

    Returns:
        str: A randomly generated short code.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@app.post(
    "/api/shorten",
    tags=["url"],
    summary="Create a short URL for a given long URL",
    status_code=status.HTTP_201_CREATED,
    response_model=ShortenResponse,
)
def create_short_url(request: ShortenRequest) -> ShortenResponse:
    """
    Creates a short URL for the given long URL.

    1. Generates a unique short code.
    2. Stores the mapping between the short code and the long URL.
    3. Constructs the short URL (assuming the domain is 'http://localhost:8000').

    Args:
        request (ShortenRequest): The request object containing the long URL.

    Returns:
        ShortenResponse: The response object containing the generated short URL.
    """
    # Generate a unique short code
    short_code = generate_short_code()
    while short_code in url_mapping:
        short_code = generate_short_code()

    # Save the mapping (replace with a persistent store in production)
    url_mapping[short_code] = request.long_url

    # Build the short URL string
    # TODO: update before deployment in production
    short_url_str = f"http://localhost:8000/{short_code}"

    # Validate and convert the string to HttpUrl using the recommended approach.
    short_url = TypeAdapter(HttpUrl).validate_python(short_url_str)

    return ShortenResponse(short_url=short_url)

from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    """
    Request model for creating/updating a short URL.
    Expects a valid URL in 'long_url'.
    """
    long_url: HttpUrl

    def get_long_url_string(self) -> str:
        return str(self.long_url)


class URLResponse(BaseModel):
    """
    Response model for returning URL information.
    Includes the short code, the corresponding long URL,
    and a constructed short URL for convenience.
    """
    id: int
    short_code: str
    long_url: HttpUrl
    short_url: HttpUrl

    class Config:
        from_attributes = True


class HealthCheck(BaseModel):
    """
    Response model for health check endpoint.
    """
    status: str

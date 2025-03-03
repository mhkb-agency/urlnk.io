import random
import string
from typing import List, cast

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import TypeAdapter, HttpUrl

from sqlalchemy.orm import Session

from ..models import URLCreate, URLResponse
from ..schemas import URL
from ..database import get_db


router = APIRouter(
    prefix="/api/urls",
    tags=["url"]
)


def generate_short_code(length: int = 6) -> str:
    """
    Generates a random string of letters and digits of the given length.
    Args:
        length (int): The length of the short code to generate.
    Returns:
        str: A randomly generated short code.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def build_short_url(short_code: str) -> str:
    """
    Builds a short URL string from the given short code.
    In production, replace 'http://localhost:8000' with your actual domain.
    """
    # TODO: update before deployment in production
    return f"http://localhost:8000/{short_code}"


@router.post(
    "",
    summary="Create a new short URL",
    status_code=status.HTTP_201_CREATED,
    response_model=URLResponse,
)
def create_short_url(
    url_data: URLCreate,
    db: Session = Depends(get_db)
) -> URLResponse:
    """
    Creates a new short URL entry in the database.

    1. Generates a unique short code.
    2. Saves the new record in the 'urls' table.
    3. Returns the saved record with a constructed short URL.
    """
    # Generate a short code and ensure uniqueness
    short_code = generate_short_code()
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    # Create a new URL record
    new_url = URL(
        short_code=short_code,
        long_url=url_data.get_long_url_string()
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    # Build the fully qualified short URL
    short_url_str = build_short_url(new_url.short_code)

    # Validate the short URL with Pydantic
    short_url_validated = TypeAdapter(HttpUrl).validate_python(short_url_str)

    return URLResponse(
        id=new_url.id,
        short_code=new_url.short_code,
        long_url=new_url.get_long_http_url(),
        short_url=short_url_validated
    )


@router.get(
    "",
    summary="Retrieve all short URLs",
    response_model=List[URLResponse],
    status_code=status.HTTP_200_OK,
)
def read_all_urls(db: Session = Depends(get_db)) -> List[URLResponse]:
    """
    Retrieves all short URL entries from the database.
    Returns a list of URLResponse objects.
    """
    urls = db.query(URL).all()
    results = []
    for url_obj in urls:
        url_obj: URL
        short_url_str = build_short_url(str(url_obj.short_code))
        short_url_validated = TypeAdapter(HttpUrl).validate_python(short_url_str)
        results.append(
            URLResponse(
                id=url_obj.id,
                short_code=str(url_obj.short_code),
                long_url=url_obj.get_long_http_url(),
                short_url=short_url_validated
            )
        )
    return results


def validate_url_and_get_response(url: URL, error_msg: str) -> URLResponse:
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_msg
        )
    short_url_str = build_short_url(url.short_code)
    short_url_validated = TypeAdapter(HttpUrl).validate_python(short_url_str)
    return URLResponse(
        id=url.id,
        short_code=url.short_code,
        long_url=url.get_long_http_url(),
        short_url=short_url_validated
    )


@router.get(
    "/{url_id}",
    summary="Retrieve a short URL by database ID",
    response_model=URLResponse,
    status_code=status.HTTP_200_OK,
)
def read_url_by_id(url_id: int, db: Session = Depends(get_db)) -> URLResponse:
    """
    Retrieves a single short URL entry from the database by its ID.
    """
    db_url = cast(URL, db.query(URL).filter(URL.id == url_id).first())
    return validate_url_and_get_response(db_url, f"URL with ID '{url_id}' not found.")


@router.get(
    "/shortcode/{short_code}",
    summary="Retrieve a short URL by short code",
    response_model=URLResponse,
    status_code=status.HTTP_200_OK,
)
def read_url_by_short_code(
    short_code: str,
    db: Session = Depends(get_db)
) -> URLResponse:
    """
    Retrieves a single short URL entry from the database by its short code.
    """
    db_url = cast(URL, db.query(URL).filter(URL.short_code == short_code).first())
    return validate_url_and_get_response(db_url, f"URL with short code '{short_code}' not found.")


@router.delete(
    "/{url_id}",
    summary="Delete a short URL by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_url_by_id(url_id: int, db: Session = Depends(get_db)) -> None:
    """
    Deletes a short URL entry from the database by its ID.
    """
    db_url = db.query(URL).filter(URL.id == url_id).first()
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"URL with ID '{url_id}' not found."
        )
    db.delete(db_url)
    db.commit()
    return


@router.put(
    "/{url_id}",
    summary="Update a short URL by ID",
    response_model=URLResponse,
    status_code=status.HTTP_200_OK,
)
def update_url_by_id(
    url_id: int,
    url_data: URLCreate,
    db: Session = Depends(get_db)
) -> URLResponse:
    """
    Updates the 'long_url' of a short URL entry in the database.
    Does not regenerate or modify the short code.
    """
    db_url = cast(URL, db.query(URL).filter(URL.id == url_id).first())
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"URL with ID '{url_id}' not found."
        )
    db_url.long_url = url_data.get_long_url_string()
    db.commit()
    db.refresh(db_url)

    short_url_str = build_short_url(db_url.short_code)
    short_url_validated = TypeAdapter(HttpUrl).validate_python(short_url_str)

    return URLResponse(
        id=db_url.id,
        short_code=db_url.short_code,
        long_url=db_url.get_long_http_url(),
        short_url=short_url_validated
    )

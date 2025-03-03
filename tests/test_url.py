from fastapi import status


def test_create_short_url(client):
    """
    Test creating a new short URL.
    Ensures the response structure and data integrity are correct.
    """
    response = client.post(
        "/api/urls",
        json={"long_url": "https://www.example.com/"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert "id" in data
    assert "short_code" in data
    assert data["long_url"] == "https://www.example.com/"
    assert data["short_url"] is not None


def test_create_short_url_bad_input(client):
    """
    Test creating a short URL with invalid data.
    Ensures it returns a 422 error.
    """
    response = client.post(
        "/api/urls",
        json={"long_url": "not-a-valid-url"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_all_urls_empty_db(client):
    """
    Test reading all URLs when there are none.
    Ensures an empty list is returned.
    """
    # Clear out any existing data before we start (not typical for production, but fine for testing).
    # This is one approach; you can also rely on the in-memory DB to be fresh each run,
    # depending on your test strategy.
    # For demonstration, we'll assume it's already empty or handle a loop of deletions.

    response = client.get("/api/urls")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Should be empty if no URLs exist
    assert isinstance(data, list)
    assert len(data) == 0


def test_read_all_urls(client):
    """
    Test reading all URLs when there is at least one URL in the database.
    """
    # Create a new URL
    create_response = client.post(
        "/api/urls",
        json={"long_url": "https://www.example1.com/"}
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    # Create a second URL
    create_response_2 = client.post(
        "/api/urls",
        json={"long_url": "https://www.example2.com/"}
    )
    assert create_response_2.status_code == status.HTTP_201_CREATED

    # Now read all
    response = client.get("/api/urls")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2  # Should have at least the two we just created

    # Optional: check if our specific URLs exist in the list
    long_urls = [url["long_url"] for url in data]
    assert "https://www.example1.com/" in long_urls
    assert "https://www.example2.com/" in long_urls


def test_read_url_by_id(client):
    """
    Test reading a single URL by its database ID.
    """
    # Create a new short URL
    create_response = client.post(
        "/api/urls",
        json={"long_url": "https://www.read-by-id.com/"}
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    created_data = create_response.json()
    url_id = created_data["id"]

    # Retrieve by that ID
    response = client.get(f"/api/urls/{url_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["id"] == url_id
    assert data["long_url"] == "https://www.read-by-id.com/"


def test_read_url_by_id_not_found(client):
    """
    Test reading a URL by ID when it does not exist.
    Ensures a 404 is returned.
    """
    response = client.get("/api/urls/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_read_url_by_short_code(client):
    """
    Test reading a single URL by its short code.
    """
    # Create a new short URL
    create_response = client.post(
        "/api/urls",
        json={"long_url": "https://www.short-code-test.com/"}
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    created_data = create_response.json()
    short_code = created_data["short_code"]

    # Retrieve by that short code
    response = client.get(f"/api/urls/shortcode/{short_code}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["short_code"] == short_code
    assert data["long_url"] == "https://www.short-code-test.com/"


def test_read_url_by_short_code_not_found(client):
    """
    Test reading a URL by short code when it does not exist.
    Ensures a 404 is returned.
    """
    response = client.get("/api/urls/shortcode/ZZZZZZ")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_update_url_by_id(client):
    """
    Test updating an existing URL by its ID.
    """
    # Create a short URL first
    create_response = client.post(
        "/api/urls",
        json={"long_url": "https://www.original.com"}
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    created_data = create_response.json()
    url_id = created_data["id"]
    original_short_code = created_data["short_code"]

    # Update the URL
    update_response = client.put(
        f"/api/urls/{url_id}",
        json={"long_url": "https://www.updated.com/"}
    )
    assert update_response.status_code == status.HTTP_200_OK
    updated_data = update_response.json()

    # Ensure ID and short_code remain the same
    assert updated_data["id"] == url_id
    assert updated_data["short_code"] == original_short_code
    # Ensure the long_url has changed
    assert updated_data["long_url"] == "https://www.updated.com/"


def test_update_url_by_id_not_found(client):
    """
    Test updating a non-existent URL by its ID returns 404.
    """
    response = client.put(
        "/api/urls/999999",
        json={"long_url": "https://www.wont-work.com"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_url_by_id(client):
    """
    Test deleting a URL by its ID.
    """
    # Create a new short URL
    create_response = client.post(
        "/api/urls",
        json={"long_url": "https://www.delete-this.com"}
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    created_data = create_response.json()
    url_id = created_data["id"]

    # Delete it
    delete_response = client.delete(f"/api/urls/{url_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Confirm it's gone
    get_response = client.get(f"/api/urls/{url_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_url_by_id_not_found(client):
    """
    Test deleting a non-existent URL returns 404.
    """
    response = client.delete("/api/urls/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

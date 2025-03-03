def test_redirect_endpoint_success(client):
    """
    Test that a valid short code returns a redirect response to the long URL.
    """
    # 1. Create a short URL first
    response_create = client.post(
        "/api/urls",
        json={"long_url": "https://www.example.com/"}
    )
    assert response_create.status_code == 201
    created_data = response_create.json()

    # 2. Request the redirect using the short code at the root ("/{short_code}")
    short_code = created_data["short_code"]
    response_redirect = client.get(f"/{short_code}", follow_redirects=False)

    # 3. Verify that we get a 302 redirect to the original URL
    assert response_redirect.status_code == 302
    assert response_redirect.headers["location"] == "https://www.example.com/"


def test_redirect_endpoint_not_found(client):
    """
    Test that a non-existent short code returns a 404 error.
    """
    response = client.get("/abc123", follow_redirects=False)
    assert response.status_code == 404
    assert response.json()["detail"] == "URL with short code 'abc123' not found."

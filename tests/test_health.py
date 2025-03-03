from fastapi import status

def test_get_health(client):
    """
    Test the health check endpoint.
    """
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "status" in data
    assert data["status"] == "OK"

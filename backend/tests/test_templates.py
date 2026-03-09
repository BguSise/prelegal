from fastapi import status


def test_list_templates(client):
    """Test listing all templates."""
    response = client.get("/api/templates")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    # Check nda-mutual exists
    template_ids = [t["id"] for t in data]
    assert "nda-mutual" in template_ids


def test_get_existing_template(client):
    """Test getting a specific template."""
    response = client.get("/api/templates/nda-mutual")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == "nda-mutual"
    assert "fields" in data
    assert "content" in data


def test_get_nonexistent_template(client):
    """Test getting a template that doesn't exist."""
    response = client.get("/api/templates/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()

from fastapi import status


def test_create_document(client, auth_headers):
    """Test creating a new document."""
    response = client.post(
        "/api/documents",
        headers=auth_headers,
        json={
            "template_id": "nda-mutual",
            "title": "Test NDA",
            "field_values": {"partyA": "Company A", "partyB": "Company B"},
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test NDA"
    assert data["template_id"] == "nda-mutual"
    assert data["status"] == "draft"
    assert "id" in data


def test_list_documents(client, auth_headers):
    """Test listing user's documents."""
    # Create a document first
    client.post(
        "/api/documents",
        headers=auth_headers,
        json={
            "template_id": "nda-mutual",
            "title": "Test NDA",
            "field_values": {},
        },
    )

    # List documents
    response = client.get("/api/documents", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == "Test NDA"


def test_get_document(client, auth_headers):
    """Test getting a specific document."""
    # Create a document first
    create_response = client.post(
        "/api/documents",
        headers=auth_headers,
        json={
            "template_id": "nda-mutual",
            "title": "Test NDA",
            "field_values": {"partyA": "Company A"},
        },
    )
    document_id = create_response.json()["id"]

    # Get the document
    response = client.get(f"/api/documents/{document_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == document_id
    assert data["title"] == "Test NDA"


def test_update_document(client, auth_headers):
    """Test updating a document."""
    # Create a document first
    create_response = client.post(
        "/api/documents",
        headers=auth_headers,
        json={
            "template_id": "nda-mutual",
            "title": "Old Title",
            "field_values": {},
        },
    )
    document_id = create_response.json()["id"]

    # Update the document
    response = client.put(
        f"/api/documents/{document_id}",
        headers=auth_headers,
        json={"title": "New Title", "field_values": {"partyA": "Updated"}},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "New Title"
    assert data["field_values"]["partyA"] == "Updated"


def test_delete_document(client, auth_headers):
    """Test deleting a document."""
    # Create a document first
    create_response = client.post(
        "/api/documents",
        headers=auth_headers,
        json={
            "template_id": "nda-mutual",
            "title": "Test NDA",
            "field_values": {},
        },
    )
    document_id = create_response.json()["id"]

    # Delete the document
    response = client.delete(f"/api/documents/{document_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify it's deleted
    response = client.get(f"/api/documents/{document_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_document_access_control(client, auth_headers, db):
    """Test that users cannot access other users' documents."""
    from app.models.user import User
    from app.services.auth_service import hash_password, create_access_token

    # Create a document with first user
    create_response = client.post(
        "/api/documents",
        headers=auth_headers,
        json={
            "template_id": "nda-mutual",
            "title": "Secret Document",
            "field_values": {},
        },
    )
    document_id = create_response.json()["id"]

    # Create second user
    user2 = User(email="user2@example.com", hashed_password=hash_password("pass123"))
    db.add(user2)
    db.commit()
    db.refresh(user2)

    # Create token for second user
    token2 = create_access_token(data={"sub": str(user2.id)})
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Try to access first user's document with second user
    response = client.get(f"/api/documents/{document_id}", headers=headers2)
    assert response.status_code == status.HTTP_403_FORBIDDEN

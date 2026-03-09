from fastapi import status


def test_register_success(client):
    """Test successful user registration."""
    response = client.post(
        "/api/auth/register",
        json={"email": "newuser@example.com", "password": "testpass123"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email(client, db):
    """Test registration with duplicate email."""
    from app.models.user import User
    from app.services.auth_service import hash_password

    # Create user in database
    user = User(email="existing@example.com", hashed_password=hash_password("pass123"))
    db.add(user)
    db.commit()

    # Try to register with same email
    response = client.post(
        "/api/auth/register",
        json={"email": "existing@example.com", "password": "newpass123"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"]


def test_login_success(client, db):
    """Test successful login."""
    from app.models.user import User
    from app.services.auth_service import hash_password

    # Create user in database
    user = User(email="login@example.com", hashed_password=hash_password("testpass123"))
    db.add(user)
    db.commit()

    # Login
    response = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "testpass123"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, db):
    """Test login with invalid credentials."""
    from app.models.user import User
    from app.services.auth_service import hash_password

    # Create user in database
    user = User(email="login@example.com", hashed_password=hash_password("testpass123"))
    db.add(user)
    db.commit()

    # Try to login with wrong password
    response = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "wrongpass"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_me_authenticated(client, auth_headers):
    """Test getting current user info when authenticated."""
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["id"] is not None
    assert data["is_active"] is True


def test_get_me_unauthenticated(client):
    """Test getting current user info without authentication."""
    response = client.get("/api/auth/me")
    assert response.status_code == status.HTTP_403_FORBIDDEN

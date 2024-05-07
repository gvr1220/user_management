import pytest
from httpx import AsyncClient
from fastapi import HTTPException, status
from app.main import app  # Import your FastAPI app
from app.models.user_model import User, UserRole
from app.dependencies import get_settings
from app.utils.security import hash_password
from app.schemas.user_schemas import UserCreate, UserResponse

settings = get_settings()

@pytest.mark.asyncio
async def test_search_users_single_field(async_client, admin_token, db_session):
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Create a test user with the username "testuser"
    test_user = User(
        nickname="testuser",
        email="testuser@example.com",
        hashed_password=hash_password("Test@Password123"),
        role=UserRole.AUTHENTICATED,
    )
    db_session.add(test_user)
    await db_session.commit()

    # Test searching by username
    username = "testuser"
    response = await async_client.get(f"/users/search?username={username}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data and isinstance(data["items"], list)
    assert len(data["items"]) == 1  # Only one user should match the search
    assert data["items"][0]["nickname"] == username

    # Test searching by email
    email = "testuser@example.com"
    response = await async_client.get(f"/users/search?email={email}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data and isinstance(data["items"], list)
    for user in data["items"]:
        assert user["email"] == email

    # Test searching by role
    role = "ADMIN"
    response = await async_client.get(f"/users/search?role={role}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data and isinstance(data["items"], list)
    for user in data["items"]:
        assert user["role"] == role


@pytest.mark.asyncio
async def test_search_users_multiple_fields_error(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    username = "testuser"
    email = "testuser@example.com"
    response = await async_client.get(f"/users/search?username={username}&email={email}", headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "Please provide input in only one search field."


@pytest.mark.asyncio
async def test_search_users_no_results(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    username = "nonexistentuser"
    response = await async_client.get(f"/users/search?username={username}", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "User not found"


@pytest.mark.asyncio
async def test_search_users_invalid_input_format(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    invalid_role = "INVALID_ROLE"
    response = await async_client.get(f"/users/search?role={invalid_role}", headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data[
               "detail"] == f"Invalid role '{invalid_role}'. Valid roles are: {', '.join([role.name for role in UserRole])}"
